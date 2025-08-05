"""BigQuery documentation crawler for optimization best practices."""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse
import hashlib

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from config.settings import get_settings
from src.common.exceptions import DocumentationCrawlerError
from src.common.logger import QueryOptimizerLogger
from src.common.models import DocumentationSection


class BigQueryDocsCrawler:
    """Crawler for BigQuery optimization documentation."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = QueryOptimizerLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BigQuery-Query-Optimizer/1.0 (Educational Purpose)'
        })
        self.crawled_urls: Set[str] = set()
        self.documentation_sections: List[DocumentationSection] = []
        
    def crawl_all_documentation(self) -> List[DocumentationSection]:
        """Crawl all BigQuery optimization documentation."""
        self.logger.logger.info("Starting BigQuery documentation crawl")
        
        try:
            # Crawl main optimization patterns
            for pattern in self.settings.documentation_patterns:
                url = f"{self.settings.docs_base_url}/{pattern}"
                self._crawl_page(url, pattern)
                time.sleep(self.settings.crawl_delay)
            
            # Crawl additional related pages
            self._crawl_related_pages()
            
            # Save documentation to disk
            self._save_documentation()
            
            self.logger.logger.info(
                "Documentation crawl completed",
                total_sections=len(self.documentation_sections),
                total_urls=len(self.crawled_urls)
            )
            
            return self.documentation_sections
            
        except Exception as e:
            self.logger.log_error(e, {"operation": "crawl_all_documentation"})
            raise DocumentationCrawlerError(f"Failed to crawl documentation: {str(e)}")
    
    def _crawl_page(self, url: str, pattern_name: str) -> Optional[DocumentationSection]:
        """Crawl a single documentation page."""
        if url in self.crawled_urls:
            return None
            
        try:
            self.logger.log_crawler_progress(url, "crawling", len(self.crawled_urls))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            content_div = soup.find('div', class_='devsite-article-body') or soup.find('main')
            if not content_div:
                self.logger.logger.warning(f"No content found for {url}")
                return None
            
            # Extract title
            title = self._extract_title(soup, pattern_name)
            
            # Convert to markdown and clean up
            content = self._extract_and_clean_content(content_div)
            
            # Extract optimization patterns mentioned
            optimization_patterns = self._extract_optimization_patterns(content)
            
            section = DocumentationSection(
                title=title,
                url=url,
                content=content,
                optimization_patterns=optimization_patterns
            )
            
            self.documentation_sections.append(section)
            self.crawled_urls.add(url)
            
            self.logger.log_crawler_progress(url, "completed", len(self.crawled_urls))
            return section
            
        except requests.RequestException as e:
            self.logger.logger.error(f"Failed to crawl {url}: {str(e)}")
            raise DocumentationCrawlerError(f"Failed to crawl {url}", url)
    
    def _crawl_related_pages(self):
        """Crawl additional related pages found in the documentation."""
        additional_urls = [
            f"{self.settings.docs_base_url}/best-practices-performance-patterns",
            f"{self.settings.docs_base_url}/sql-best-practices",
            f"{self.settings.docs_base_url}/query-optimization-techniques",
            f"{self.settings.docs_base_url}/performance-troubleshooting",
            f"{self.settings.docs_base_url}/controlling-costs",
            f"{self.settings.docs_base_url}/optimizing-storage",
        ]
        
        for url in additional_urls:
            try:
                self._crawl_page(url, "additional")
                time.sleep(self.settings.crawl_delay)
            except DocumentationCrawlerError:
                # Continue with other URLs if one fails
                continue
    
    def _extract_title(self, soup: BeautifulSoup, pattern_name: str) -> str:
        """Extract page title."""
        title_tag = soup.find('h1') or soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        return pattern_name.replace('-', ' ').title()
    
    def _extract_and_clean_content(self, content_div) -> str:
        """Extract and clean content from HTML."""
        # Remove navigation and other non-content elements
        for element in content_div.find_all(['nav', 'aside', 'footer', 'header']):
            element.decompose()
        
        # Remove script and style elements
        for element in content_div.find_all(['script', 'style']):
            element.decompose()
        
        # Convert to markdown
        content = md(str(content_div), heading_style="ATX")
        
        # Clean up the markdown
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('```') or line.startswith('```sql'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _extract_optimization_patterns(self, content: str) -> List[str]:
        """Extract optimization patterns mentioned in the content."""
        patterns = []
        
        # Common optimization keywords to look for
        optimization_keywords = {
            'join': ['JOIN optimization', 'join reordering', 'join performance'],
            'partition': ['partition filtering', 'partitioned tables', 'partition pruning'],
            'cluster': ['clustering', 'clustered tables', 'cluster keys'],
            'subquery': ['subquery optimization', 'correlated subqueries'],
            'window': ['window functions', 'window optimization'],
            'aggregate': ['aggregation', 'GROUP BY optimization'],
            'index': ['indexing', 'secondary indexes'],
            'materialized': ['materialized views', 'view optimization'],
            'approximate': ['approximate aggregation', 'HyperLogLog'],
            'predicate': ['predicate pushdown', 'filter optimization']
        }
        
        content_lower = content.lower()
        
        for category, keywords in optimization_keywords.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    patterns.append(keyword)
        
        return list(set(patterns))  # Remove duplicates
    
    def _save_documentation(self):
        """Save crawled documentation to disk."""
        output_dir = self.settings.docs_output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save individual sections
        for section in self.documentation_sections:
            filename = self._generate_filename(section.title, section.url)
            file_path = output_dir / f"{filename}.json"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(section.model_dump(), f, indent=2, default=str)
        
        # Save summary index
        index_data = {
            'crawl_timestamp': time.time(),
            'total_sections': len(self.documentation_sections),
            'sections': [
                {
                    'title': section.title,
                    'url': section.url,
                    'patterns': section.optimization_patterns,
                    'content_length': len(section.content)
                }
                for section in self.documentation_sections
            ]
        }
        
        with open(output_dir / 'index.json', 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
        
        self.logger.logger.info(f"Documentation saved to {output_dir}")
    
    def _generate_filename(self, title: str, url: str) -> str:
        """Generate a safe filename from title and URL."""
        # Create a hash of the URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # Clean title for filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_').lower()[:50]  # Limit length
        
        return f"{safe_title}_{url_hash}"
    
    def load_cached_documentation(self) -> List[DocumentationSection]:
        """Load previously crawled documentation from disk."""
        output_dir = self.settings.docs_output_dir
        
        if not output_dir.exists():
            return []
        
        sections = []
        for json_file in output_dir.glob('*.json'):
            if json_file.name == 'index.json':
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    section = DocumentationSection(**data)
                    sections.append(section)
            except Exception as e:
                self.logger.logger.warning(f"Failed to load {json_file}: {str(e)}")
        
        self.logger.logger.info(f"Loaded {len(sections)} cached documentation sections")
        return sections
    
    def is_cache_fresh(self, max_age_hours: int = 24) -> bool:
        """Check if cached documentation is fresh enough."""
        index_file = self.settings.docs_output_dir / 'index.json'
        
        if not index_file.exists():
            return False
        
        try:
            with open(index_file, 'r') as f:
                index_data = json.load(f)
                crawl_time = index_data.get('crawl_timestamp', 0)
                age_hours = (time.time() - crawl_time) / 3600
                return age_hours < max_age_hours
        except Exception:
            return False


def main():
    """Main function for running the crawler standalone."""
    crawler = BigQueryDocsCrawler()
    
    # Check if we have fresh cached data
    if crawler.is_cache_fresh():
        print("Using cached documentation (less than 24 hours old)")
        sections = crawler.load_cached_documentation()
    else:
        print("Crawling fresh documentation...")
        sections = crawler.crawl_all_documentation()
    
    print(f"Total documentation sections: {len(sections)}")
    for section in sections:
        print(f"- {section.title} ({len(section.optimization_patterns)} patterns)")


if __name__ == "__main__":
    main()