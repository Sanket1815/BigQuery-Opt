#!/usr/bin/env python3
"""
Documentation crawler script for BigQuery optimization best practices.
Crawls Google Cloud BigQuery documentation and creates a searchable knowledge base.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from src.crawler.bigquery_docs_crawler import BigQueryDocsCrawler
    from src.crawler.documentation_processor import DocumentationProcessor
    from config.settings import get_settings
    from src.common.logger import QueryOptimizerLogger
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


class DocumentationCrawlerScript:
    """Main documentation crawler script with comprehensive features."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        self.crawler = BigQueryDocsCrawler()
        
        try:
            self.processor = DocumentationProcessor()
        except ImportError:
            print("⚠️ DocumentationProcessor not available - will skip embedding generation")
            self.processor = None
    
    def crawl_all_documentation(self, force_refresh: bool = False) -> bool:
        """Crawl all BigQuery documentation."""
        
        print("🚀 BigQuery Documentation Crawler")
        print("=" * 60)
        print("🎯 Purpose: Create searchable knowledge base of BigQuery optimization patterns")
        print("📚 Source: Google Cloud BigQuery Documentation")
        print("🔍 Patterns: 20+ distinct optimization techniques")
        print("=" * 60)
        
        try:
            # Check if we have fresh cached documentation
            if not force_refresh and self.crawler.is_cache_fresh(max_age_hours=24):
                print("📋 Using cached documentation (less than 24 hours old)")
                sections = self.crawler.load_cached_documentation()
                
                if sections:
                    print(f"✅ Loaded {len(sections)} cached documentation sections")
                    self._display_documentation_summary(sections)
                    return True
                else:
                    print("⚠️ No cached documentation found, proceeding with fresh crawl")
            
            # Crawl fresh documentation
            print("🕷️ Starting fresh documentation crawl...")
            print("⏱️ This may take a few minutes to respect rate limits")
            
            start_time = time.time()
            sections = self.crawler.crawl_all_documentation()
            crawl_time = time.time() - start_time
            
            print(f"\n✅ Documentation crawl completed!")
            print(f"⏱️ Total time: {crawl_time:.1f} seconds")
            print(f"📄 Sections crawled: {len(sections)}")
            
            self._display_documentation_summary(sections)
            
            # Process documentation for semantic search
            if self.processor:
                print(f"\n🧠 Processing documentation for semantic search...")
                self.processor.process_documentation(sections)
                print(f"✅ Documentation processing completed")
                
                # Test semantic search
                self._test_semantic_search()
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "crawl_all_documentation"})
            print(f"❌ Documentation crawl failed: {str(e)}")
            return False
    
    def _display_documentation_summary(self, sections: List) -> None:
        """Display summary of crawled documentation."""
        
        print(f"\n📊 DOCUMENTATION SUMMARY")
        print(f"-" * 40)
        
        # Count patterns by type
        pattern_counts = {}
        total_content_length = 0
        
        for section in sections:
            total_content_length += len(section.content)
            
            for pattern in section.optimization_patterns:
                pattern_type = self._categorize_pattern(pattern)
                pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        print(f"📄 Total sections: {len(sections)}")
        print(f"📝 Total content: {total_content_length:,} characters")
        print(f"🔍 Optimization patterns found:")
        
        for pattern_type, count in sorted(pattern_counts.items()):
            print(f"   • {pattern_type}: {count} references")
        
        print(f"\n📚 Documentation sections:")
        for i, section in enumerate(sections[:10], 1):  # Show first 10
            patterns_text = ", ".join(section.optimization_patterns[:3])
            if len(section.optimization_patterns) > 3:
                patterns_text += f" (+{len(section.optimization_patterns) - 3} more)"
            
            print(f"   {i:2d}. {section.title}")
            print(f"       📊 {len(section.content):,} chars | 🔍 Patterns: {patterns_text}")
        
        if len(sections) > 10:
            print(f"       ... and {len(sections) - 10} more sections")
    
    def _categorize_pattern(self, pattern: str) -> str:
        """Categorize optimization pattern by type."""
        pattern_lower = pattern.lower()
        
        if any(word in pattern_lower for word in ['join', 'inner', 'left', 'right']):
            return "JOIN Optimization"
        elif any(word in pattern_lower for word in ['partition', 'partitioned']):
            return "Partition Optimization"
        elif any(word in pattern_lower for word in ['cluster', 'clustering']):
            return "Clustering Optimization"
        elif any(word in pattern_lower for word in ['subquery', 'exists', 'correlated']):
            return "Subquery Optimization"
        elif any(word in pattern_lower for word in ['window', 'over', 'rank']):
            return "Window Function Optimization"
        elif any(word in pattern_lower for word in ['aggregate', 'group by', 'count', 'sum']):
            return "Aggregation Optimization"
        elif any(word in pattern_lower for word in ['approximate', 'approx']):
            return "Approximate Function Optimization"
        elif any(word in pattern_lower for word in ['materialized', 'view']):
            return "Materialized View Optimization"
        else:
            return "General Optimization"
    
    def _test_semantic_search(self) -> None:
        """Test semantic search functionality."""
        
        if not self.processor:
            return
        
        print(f"\n🔍 Testing semantic search functionality...")
        
        test_queries = [
            "How to optimize JOIN performance?",
            "Best practices for large table scans",
            "Reducing BigQuery costs",
            "Window function optimization",
            "Approximate aggregation functions"
        ]
        
        for query in test_queries:
            try:
                results = self.processor.search_documentation(query, n_results=3)
                
                if results:
                    print(f"\n🔍 Query: '{query}'")
                    for i, result in enumerate(results, 1):
                        score = result.get('similarity_score', 0)
                        patterns = result.get('optimization_patterns', [])
                        print(f"   {i}. {result['title']} (score: {score:.3f})")
                        if patterns:
                            print(f"      Patterns: {', '.join(patterns[:3])}")
                else:
                    print(f"⚠️ No results for: '{query}'")
                    
            except Exception as e:
                print(f"❌ Search failed for '{query}': {e}")
        
        # Get summary
        try:
            summary = self.processor.get_documentation_summary()
            print(f"\n📊 Vector Database Summary:")
            print(f"   📄 Document chunks: {summary.get('total_chunks', 0)}")
            print(f"   🔍 Optimization patterns: {summary.get('optimization_patterns', 0)}")
            print(f"   🧠 Embedding model: {summary.get('embedding_model', 'Unknown')}")
        except Exception as e:
            print(f"⚠️ Could not get summary: {e}")
    
    def update_documentation(self) -> bool:
        """Update documentation with latest changes."""
        
        print("🔄 Updating documentation...")
        
        # Force refresh of documentation
        return self.crawl_all_documentation(force_refresh=True)
    
    def validate_documentation(self) -> bool:
        """Validate crawled documentation quality."""
        
        print("✅ Validating documentation quality...")
        
        try:
            sections = self.crawler.load_cached_documentation()
            
            if not sections:
                print("❌ No documentation found to validate")
                return False
            
            validation_results = {
                "total_sections": len(sections),
                "sections_with_patterns": 0,
                "total_patterns": 0,
                "avg_content_length": 0,
                "sections_with_urls": 0
            }
            
            total_content = 0
            unique_patterns = set()
            
            for section in sections:
                total_content += len(section.content)
                
                if section.optimization_patterns:
                    validation_results["sections_with_patterns"] += 1
                    unique_patterns.update(section.optimization_patterns)
                
                if hasattr(section, 'url') and section.url:
                    validation_results["sections_with_urls"] += 1
            
            validation_results["total_patterns"] = len(unique_patterns)
            validation_results["avg_content_length"] = total_content // len(sections)
            
            # Display validation results
            print(f"📊 Documentation Validation Results:")
            print(f"   📄 Total sections: {validation_results['total_sections']}")
            print(f"   🔍 Sections with patterns: {validation_results['sections_with_patterns']}")
            print(f"   📋 Unique patterns found: {validation_results['total_patterns']}")
            print(f"   📝 Average content length: {validation_results['avg_content_length']:,} chars")
            print(f"   🔗 Sections with URLs: {validation_results['sections_with_urls']}")
            
            # Quality checks
            quality_score = 0
            max_score = 5
            
            if validation_results["total_sections"] >= 10:
                quality_score += 1
                print("   ✅ Sufficient sections (10+)")
            else:
                print("   ❌ Insufficient sections (<10)")
            
            if validation_results["total_patterns"] >= 20:
                quality_score += 1
                print("   ✅ Sufficient patterns (20+)")
            else:
                print("   ❌ Insufficient patterns (<20)")
            
            if validation_results["avg_content_length"] >= 500:
                quality_score += 1
                print("   ✅ Good content depth (500+ chars avg)")
            else:
                print("   ❌ Shallow content (<500 chars avg)")
            
            pattern_coverage = validation_results["sections_with_patterns"] / validation_results["total_sections"]
            if pattern_coverage >= 0.7:
                quality_score += 1
                print(f"   ✅ Good pattern coverage ({pattern_coverage:.1%})")
            else:
                print(f"   ❌ Low pattern coverage ({pattern_coverage:.1%})")
            
            url_coverage = validation_results["sections_with_urls"] / validation_results["total_sections"]
            if url_coverage >= 0.8:
                quality_score += 1
                print(f"   ✅ Good URL coverage ({url_coverage:.1%})")
            else:
                print(f"   ❌ Low URL coverage ({url_coverage:.1%})")
            
            print(f"\n🎯 Overall Quality Score: {quality_score}/{max_score}")
            
            if quality_score >= 4:
                print("✅ Documentation quality is EXCELLENT")
                return True
            elif quality_score >= 3:
                print("⚠️ Documentation quality is GOOD but could be improved")
                return True
            else:
                print("❌ Documentation quality is POOR - consider re-crawling")
                return False
                
        except Exception as e:
            self.logger.log_error(e, {"operation": "validate_documentation"})
            print(f"❌ Documentation validation failed: {str(e)}")
            return False
    
    def export_documentation(self, output_format: str = "json", output_file: str = None) -> bool:
        """Export documentation in various formats."""
        
        try:
            sections = self.crawler.load_cached_documentation()
            
            if not sections:
                print("❌ No documentation found to export")
                return False
            
            if not output_file:
                timestamp = int(time.time())
                output_file = f"bigquery_docs_export_{timestamp}.{output_format}"
            
            print(f"📤 Exporting documentation to {output_file}...")
            
            if output_format == "json":
                self._export_json(sections, output_file)
            elif output_format == "markdown":
                self._export_markdown(sections, output_file)
            elif output_format == "csv":
                self._export_csv(sections, output_file)
            else:
                print(f"❌ Unsupported format: {output_format}")
                return False
            
            print(f"✅ Documentation exported successfully to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {str(e)}")
            return False
    
    def _export_json(self, sections: List, output_file: str) -> None:
        """Export documentation as JSON."""
        import json
        
        export_data = {
            "export_timestamp": time.time(),
            "total_sections": len(sections),
            "sections": [section.model_dump() for section in sections]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
    
    def _export_markdown(self, sections: List, output_file: str) -> None:
        """Export documentation as markdown."""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# BigQuery Optimization Documentation\n\n")
            f.write(f"Exported on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total sections: {len(sections)}\n\n")
            
            for i, section in enumerate(sections, 1):
                f.write(f"## {i}. {section.title}\n\n")
                f.write(f"**URL**: {getattr(section, 'url', 'N/A')}\n\n")
                
                if section.optimization_patterns:
                    f.write(f"**Optimization Patterns**: {', '.join(section.optimization_patterns)}\n\n")
                
                f.write(f"{section.content}\n\n")
                f.write("---\n\n")
    
    def _export_csv(self, sections: List, output_file: str) -> None:
        """Export documentation as CSV."""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'URL', 'Content_Length', 'Optimization_Patterns', 'Content_Preview'])
            
            for section in sections:
                patterns = '; '.join(section.optimization_patterns)
                content_preview = section.content[:200].replace('\n', ' ') + '...'
                
                writer.writerow([
                    section.title,
                    getattr(section, 'url', ''),
                    len(section.content),
                    patterns,
                    content_preview
                ])
    
    def search_documentation(self, query: str, n_results: int = 5) -> None:
        """Search documentation for specific topics."""
        
        if not self.processor:
            print("❌ Documentation processor not available")
            return
        
        print(f"🔍 Searching documentation for: '{query}'")
        print("-" * 50)
        
        try:
            results = self.processor.search_documentation(query, n_results)
            
            if results:
                for i, result in enumerate(results, 1):
                    score = result.get('similarity_score', 0)
                    patterns = result.get('optimization_patterns', [])
                    
                    print(f"{i}. {result['title']}")
                    print(f"   📊 Relevance: {score:.3f}")
                    print(f"   🔗 URL: {result.get('url', 'N/A')}")
                    
                    if patterns:
                        print(f"   🔍 Patterns: {', '.join(patterns[:5])}")
                        if len(patterns) > 5:
                            print(f"              (+{len(patterns) - 5} more)")
                    
                    content_preview = result['content'][:200].replace('\n', ' ')
                    print(f"   📝 Preview: {content_preview}...")
                    print()
            else:
                print("❌ No results found")
                
        except Exception as e:
            print(f"❌ Search failed: {str(e)}")
    
    def list_optimization_patterns(self) -> None:
        """List all available optimization patterns."""
        
        if not self.processor:
            print("❌ Documentation processor not available")
            return
        
        print("🔍 Available Optimization Patterns")
        print("=" * 50)
        
        try:
            patterns = self.processor.optimization_patterns
            
            if patterns:
                for i, pattern in enumerate(patterns, 1):
                    improvement = pattern.expected_improvement or 0
                    print(f"{i:2d}. {pattern.name}")
                    print(f"    📊 Expected improvement: {improvement:.1%}")
                    print(f"    📝 Description: {pattern.description}")
                    print(f"    🔗 Documentation: {pattern.documentation_url}")
                    print(f"    🎯 Applies to: {', '.join(pattern.applicability_conditions[:3])}")
                    print()
                
                print(f"📊 Total patterns: {len(patterns)}")
            else:
                print("❌ No optimization patterns found")
                
        except Exception as e:
            print(f"❌ Failed to list patterns: {str(e)}")
    
    def get_crawl_status(self) -> Dict[str, Any]:
        """Get current crawl status and statistics."""
        
        try:
            # Check cache status
            cache_fresh = self.crawler.is_cache_fresh()
            
            # Load sections
            sections = self.crawler.load_cached_documentation()
            
            # Get processor status
            processor_status = {}
            if self.processor:
                try:
                    processor_status = self.processor.get_documentation_summary()
                except Exception as e:
                    processor_status = {"error": str(e)}
            
            status = {
                "cache_fresh": cache_fresh,
                "cached_sections": len(sections),
                "last_crawl": "Unknown",
                "processor_status": processor_status,
                "patterns_available": len(self.processor.optimization_patterns) if self.processor else 0
            }
            
            # Try to get last crawl time
            try:
                index_file = self.settings.docs_output_dir / 'index.json'
                if index_file.exists():
                    import json
                    with open(index_file, 'r') as f:
                        index_data = json.load(f)
                        crawl_timestamp = index_data.get('crawl_timestamp', 0)
                        status["last_crawl"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(crawl_timestamp))
            except Exception:
                pass
            
            return status
            
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main function for documentation crawler script."""
    
    parser = argparse.ArgumentParser(description="BigQuery Documentation Crawler")
    parser.add_argument(
        "action",
        choices=["crawl", "update", "validate", "export", "search", "patterns", "status"],
        help="Action to perform"
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force refresh even if cache is fresh"
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "markdown", "csv"],
        default="json",
        help="Export format (for export action)"
    )
    parser.add_argument(
        "--output-file",
        help="Output file path (for export action)"
    )
    parser.add_argument(
        "--query",
        help="Search query (for search action)"
    )
    parser.add_argument(
        "--results",
        type=int,
        default=5,
        help="Number of search results (for search action)"
    )
    
    args = parser.parse_args()
    
    # Initialize crawler
    try:
        crawler_script = DocumentationCrawlerScript()
    except Exception as e:
        print(f"❌ Failed to initialize crawler: {e}")
        sys.exit(1)
    
    # Execute requested action
    success = True
    
    if args.action == "crawl":
        success = crawler_script.crawl_all_documentation(args.force_refresh)
    
    elif args.action == "update":
        success = crawler_script.update_documentation()
    
    elif args.action == "validate":
        success = crawler_script.validate_documentation()
    
    elif args.action == "export":
        success = crawler_script.export_documentation(args.output_format, args.output_file)
    
    elif args.action == "search":
        if not args.query:
            print("❌ Search query required. Use --query 'your search terms'")
            sys.exit(1)
        crawler_script.search_documentation(args.query, args.results)
    
    elif args.action == "patterns":
        crawler_script.list_optimization_patterns()
    
    elif args.action == "status":
        status = crawler_script.get_crawl_status()
        print("📊 Documentation Crawler Status")
        print("=" * 40)
        for key, value in status.items():
            print(f"{key}: {value}")
    
    # Exit with appropriate code
    if args.action in ["crawl", "update", "validate", "export"]:
        sys.exit(0 if success else 1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()