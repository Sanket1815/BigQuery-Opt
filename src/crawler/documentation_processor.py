"""Documentation processor for creating embeddings and preparing data for MCP server."""

import json
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

from config.settings import get_settings
from src.common.exceptions import DocumentationCrawlerError
from src.common.logger import QueryOptimizerLogger
from src.common.models import DocumentationSection, OptimizationPattern, OptimizationType


class DocumentationProcessor:
    """Processes crawled documentation and creates embeddings for semantic search."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        self.embedding_model = SentenceTransformer(self.settings.embedding_model)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.settings.vector_db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create or get collection
        self.collection = self._get_or_create_collection()
        
        # Load optimization patterns
        self.optimization_patterns = self._load_optimization_patterns()
    
    def _get_or_create_collection(self):
        """Get or create ChromaDB collection for documentation."""
        try:
            collection = self.chroma_client.get_collection("bigquery_docs")
        except ValueError:
            # Collection doesn't exist, create it
            collection = self.chroma_client.create_collection(
                name="bigquery_docs",
                metadata={"description": "BigQuery optimization documentation"}
            )
        return collection
    
    def process_documentation(self, sections: List[DocumentationSection]) -> None:
        """Process documentation sections and create embeddings."""
        self.logger.logger.info(f"Processing {len(sections)} documentation sections")
        
        # Clear existing data
        self.collection.delete()
        
        documents = []
        metadatas = []
        ids = []
        
        for i, section in enumerate(sections):
            # Split content into chunks for better retrieval
            chunks = self._split_content(section.content)
            
            for j, chunk in enumerate(chunks):
                doc_id = f"{i}_{j}"
                
                documents.append(chunk)
                metadatas.append({
                    "title": section.title,
                    "url": section.url,
                    "chunk_index": j,
                    "total_chunks": len(chunks),
                    "optimization_patterns": json.dumps(section.optimization_patterns),
                    "content_length": len(chunk)
                })
                ids.append(doc_id)
        
        # Create embeddings and store in ChromaDB
        self.logger.logger.info(f"Creating embeddings for {len(documents)} document chunks")
        
        # Process in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_metas = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            self.collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )
        
        self.logger.logger.info("Documentation processing completed")
    
    def _split_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into smaller chunks for better retrieval."""
        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def search_documentation(
        self, 
        query: str, 
        n_results: int = 5,
        filter_patterns: Optional[List[str]] = None
    ) -> List[Dict]:
        """Search documentation using semantic similarity."""
        try:
            # Perform semantic search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if results['distances'] else None
                    
                    # Filter by patterns if specified
                    if filter_patterns:
                        doc_patterns = json.loads(metadata.get('optimization_patterns', '[]'))
                        if not any(pattern in doc_patterns for pattern in filter_patterns):
                            continue
                    
                    search_results.append({
                        'content': doc,
                        'title': metadata['title'],
                        'url': metadata['url'],
                        'chunk_index': metadata['chunk_index'],
                        'optimization_patterns': json.loads(metadata.get('optimization_patterns', '[]')),
                        'similarity_score': 1 - distance if distance else None
                    })
            
            return search_results
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "search_documentation", "query": query})
            return []
    
    def get_optimization_patterns_for_query(self, query: str) -> List[OptimizationPattern]:
        """Get relevant optimization patterns for a SQL query."""
        relevant_patterns = []
        
        # Search for relevant documentation
        search_results = self.search_documentation(query, n_results=10)
        
        # Extract patterns mentioned in the results
        mentioned_patterns = set()
        for result in search_results:
            mentioned_patterns.update(result['optimization_patterns'])
        
        # Match with our predefined patterns
        for pattern in self.optimization_patterns:
            if any(keyword.lower() in query.lower() for keyword in pattern.applicability_conditions):
                relevant_patterns.append(pattern)
            elif pattern.name in mentioned_patterns:
                relevant_patterns.append(pattern)
        
        return relevant_patterns
    
    def _load_optimization_patterns(self) -> List[OptimizationPattern]:
        """Load predefined optimization patterns."""
        patterns = [
            OptimizationPattern(
                pattern_id="join_reordering",
                name="JOIN Reordering",
                description="Reorder JOINs to place smaller tables first and use more selective filters early",
                optimization_type=OptimizationType.JOIN_REORDERING,
                documentation_url="https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns",
                expected_improvement=0.3,
                applicability_conditions=["JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN"],
                sql_pattern=r".*JOIN.*",
                replacement_pattern="Reorder tables by size and selectivity"
            ),
            OptimizationPattern(
                pattern_id="partition_filtering",
                name="Partition Filtering",
                description="Add partition filters to reduce the amount of data scanned",
                optimization_type=OptimizationType.PARTITION_FILTERING,
                documentation_url="https://cloud.google.com/bigquery/docs/partitioned-tables",
                expected_improvement=0.5,
                applicability_conditions=["WHERE", "partitioned table", "_PARTITIONTIME", "_PARTITIONDATE"],
                sql_pattern=r"FROM\s+\w+\.\w+\.\w+",
                replacement_pattern="Add WHERE _PARTITIONDATE >= 'YYYY-MM-DD'"
            ),
            OptimizationPattern(
                pattern_id="subquery_to_join",
                name="Subquery to JOIN Conversion",
                description="Convert correlated subqueries to JOINs for better performance",
                optimization_type=OptimizationType.SUBQUERY_CONVERSION,
                documentation_url="https://cloud.google.com/bigquery/docs/best-practices-performance-compute#avoid_oversharding_tables",
                expected_improvement=0.4,
                applicability_conditions=["EXISTS", "IN (SELECT", "correlated subquery"],
                sql_pattern=r"WHERE.*EXISTS\s*\(SELECT.*\)",
                replacement_pattern="Convert to INNER JOIN or LEFT JOIN"
            ),
            OptimizationPattern(
                pattern_id="window_optimization",
                name="Window Function Optimization",
                description="Optimize window function specifications and partitioning",
                optimization_type=OptimizationType.WINDOW_OPTIMIZATION,
                documentation_url="https://cloud.google.com/bigquery/docs/reference/standard-sql/analytic-functions",
                expected_improvement=0.25,
                applicability_conditions=["OVER (", "ROW_NUMBER", "RANK", "DENSE_RANK", "LAG", "LEAD"],
                sql_pattern=r".*OVER\s*\(",
                replacement_pattern="Optimize PARTITION BY and ORDER BY clauses"
            ),
            OptimizationPattern(
                pattern_id="approximate_aggregation",
                name="Approximate Aggregation",
                description="Use approximate aggregation functions for better performance",
                optimization_type=OptimizationType.APPROXIMATE_AGGREGATION,
                documentation_url="https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions",
                expected_improvement=0.6,
                applicability_conditions=["COUNT(DISTINCT", "large dataset", "approximate"],
                sql_pattern=r"COUNT\s*\(\s*DISTINCT",
                replacement_pattern="Use APPROX_COUNT_DISTINCT() instead"
            ),
            OptimizationPattern(
                pattern_id="column_pruning",
                name="Column Pruning",
                description="Select only necessary columns to reduce data transfer",
                optimization_type=OptimizationType.COLUMN_PRUNING,
                documentation_url="https://cloud.google.com/bigquery/docs/best-practices-performance-input",
                expected_improvement=0.2,
                applicability_conditions=["SELECT *", "unnecessary columns"],
                sql_pattern=r"SELECT\s+\*",
                replacement_pattern="SELECT specific columns instead of *"
            ),
            OptimizationPattern(
                pattern_id="predicate_pushdown",
                name="Predicate Pushdown",
                description="Move filter conditions closer to data sources",
                optimization_type=OptimizationType.PREDICATE_PUSHDOWN,
                documentation_url="https://cloud.google.com/bigquery/docs/best-practices-performance-compute",
                expected_improvement=0.35,
                applicability_conditions=["WHERE", "HAVING", "filter"],
                sql_pattern=r"WHERE.*",
                replacement_pattern="Apply filters as early as possible in the query"
            ),
            OptimizationPattern(
                pattern_id="clustering_optimization",
                name="Clustering Optimization",
                description="Use clustered tables and optimize clustering keys",
                optimization_type=OptimizationType.CLUSTERING_RECOMMENDATION,
                documentation_url="https://cloud.google.com/bigquery/docs/clustered-tables",
                expected_improvement=0.4,
                applicability_conditions=["clustered table", "WHERE", "ORDER BY"],
                sql_pattern=r"WHERE.*=.*",
                replacement_pattern="Ensure WHERE clauses use clustering keys"
            ),
            OptimizationPattern(
                pattern_id="materialized_view",
                name="Materialized View Suggestion",
                description="Suggest using materialized views for frequently accessed data",
                optimization_type=OptimizationType.MATERIALIZED_VIEW_SUGGESTION,
                documentation_url="https://cloud.google.com/bigquery/docs/materialized-views-intro",
                expected_improvement=0.7,
                applicability_conditions=["frequent query", "aggregation", "GROUP BY"],
                sql_pattern=r"GROUP BY.*",
                replacement_pattern="Consider creating a materialized view"
            )
        ]
        
        return patterns
    
    def get_pattern_by_id(self, pattern_id: str) -> Optional[OptimizationPattern]:
        """Get optimization pattern by ID."""
        for pattern in self.optimization_patterns:
            if pattern.pattern_id == pattern_id:
                return pattern
        return None
    
    def get_documentation_summary(self) -> Dict:
        """Get summary of processed documentation."""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "optimization_patterns": len(self.optimization_patterns),
                "embedding_model": self.settings.embedding_model,
                "vector_db_path": str(self.settings.vector_db_path)
            }
        except Exception as e:
            self.logger.log_error(e, {"operation": "get_documentation_summary"})
            return {"error": str(e)}


def main():
    """Main function for processing documentation."""
    from src.crawler.bigquery_docs_crawler import BigQueryDocsCrawler
    
    # Load documentation
    crawler = BigQueryDocsCrawler()
    if crawler.is_cache_fresh():
        sections = crawler.load_cached_documentation()
    else:
        sections = crawler.crawl_all_documentation()
    
    if not sections:
        print("No documentation found. Please run the crawler first.")
        return
    
    # Process documentation
    processor = DocumentationProcessor()
    processor.process_documentation(sections)
    
    # Test search
    test_query = "optimize JOIN performance"
    results = processor.search_documentation(test_query, n_results=3)
    
    print(f"Test search for '{test_query}':")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']} (score: {result['similarity_score']:.3f})")
        print(f"   Patterns: {result['optimization_patterns']}")
        print(f"   Content: {result['content'][:200]}...")
        print()
    
    # Show summary
    summary = processor.get_documentation_summary()
    print(f"Documentation summary: {summary}")


if __name__ == "__main__":
    main()