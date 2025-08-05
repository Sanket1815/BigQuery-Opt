"""Command-line interface for BigQuery Query Optimizer."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from config.settings import get_settings
from src.optimizer.query_optimizer import BigQueryOptimizer
from src.common.exceptions import OptimizationError, BigQueryConnectionError


console = Console()


@click.group()
@click.option('--project-id', help='Google Cloud Project ID')
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.pass_context
def cli(ctx, project_id: Optional[str], debug: bool):
    """BigQuery Query Optimizer - AI-powered SQL optimization tool."""
    ctx.ensure_object(dict)
    ctx.obj['project_id'] = project_id
    ctx.obj['debug'] = debug
    
    if debug:
        console.print("[yellow]Debug mode enabled[/yellow]")


@cli.command()
@click.option('--query', '-q', help='SQL query to optimize')
@click.option('--file', '-f', type=click.Path(exists=True), help='File containing SQL query')
@click.option('--output', '-o', type=click.Path(), help='Output file for optimized query')
@click.option('--validate/--no-validate', default=True, help='Validate query results')
@click.option('--measure-performance/--no-performance', default=False, help='Measure actual performance')
@click.option('--sample-size', type=int, default=1000, help='Sample size for validation')
@click.option('--format', type=click.Choice(['json', 'text', 'table']), default='text', help='Output format')
@click.pass_context
def optimize(ctx, query: Optional[str], file: Optional[str], output: Optional[str], 
             validate: bool, measure_performance: bool, sample_size: int, format: str):
    """Optimize a BigQuery SQL query."""
    
    try:
        # Get query from parameter or file
        if query:
            sql_query = query
        elif file:
            with open(file, 'r') as f:
                sql_query = f.read()
        else:
            console.print("[red]Error: Must provide either --query or --file[/red]")
            sys.exit(1)
        
        console.print(f"[blue]Optimizing query ({len(sql_query)} characters)...[/blue]")
        
        # Initialize optimizer
        optimizer = BigQueryOptimizer(
            project_id=ctx.obj.get('project_id'),
            validate_results=validate
        )
        
        # Test connection
        if not optimizer.test_connection():
            console.print("[red]Error: Failed to connect to required services[/red]")
            sys.exit(1)
        
        # Optimize query
        with console.status("[bold green]Optimizing query..."):
            result = optimizer.optimize_query(
                sql_query,
                validate_results=validate,
                measure_performance=measure_performance,
                sample_size=sample_size
            )
        
        # Output results
        if format == 'json':
            output_data = result.model_dump()
            if output:
                with open(output, 'w') as f:
                    json.dump(output_data, f, indent=2, default=str)
                console.print(f"[green]Results saved to {output}[/green]")
            else:
                console.print_json(data=output_data)
        
        elif format == 'table':
            _display_optimization_table(result)
        
        else:  # text format
            _display_optimization_text(result, output)
        
        # Exit with appropriate code
        if result.validation_error:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('debug'):
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.option('--query', '-q', help='SQL query to analyze')
@click.option('--file', '-f', type=click.Path(exists=True), help='File containing SQL query')
@click.pass_context
def analyze(ctx, query: Optional[str], file: Optional[str]):
    """Analyze a query without optimizing it."""
    
    try:
        # Get query from parameter or file
        if query:
            sql_query = query
        elif file:
            with open(file, 'r') as f:
                sql_query = f.read()
        else:
            console.print("[red]Error: Must provide either --query or --file[/red]")
            sys.exit(1)
        
        # Initialize optimizer
        optimizer = BigQueryOptimizer(project_id=ctx.obj.get('project_id'))
        
        # Analyze query
        with console.status("[bold green]Analyzing query..."):
            analysis = optimizer.analyze_query_only(sql_query)
        
        # Display analysis
        _display_query_analysis(analysis)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('debug'):
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.option('--original', '-o', help='Original SQL query')
@click.option('--optimized', '-p', help='Optimized SQL query')
@click.option('--original-file', type=click.Path(exists=True), help='File with original query')
@click.option('--optimized-file', type=click.Path(exists=True), help='File with optimized query')
@click.option('--sample-size', type=int, default=1000, help='Sample size for validation')
@click.pass_context
def validate(ctx, original: Optional[str], optimized: Optional[str], 
             original_file: Optional[str], optimized_file: Optional[str], sample_size: int):
    """Validate that optimized query returns identical results."""
    
    try:
        # Get queries
        if original and optimized:
            original_query = original
            optimized_query = optimized
        elif original_file and optimized_file:
            with open(original_file, 'r') as f:
                original_query = f.read()
            with open(optimized_file, 'r') as f:
                optimized_query = f.read()
        else:
            console.print("[red]Error: Must provide both original and optimized queries[/red]")
            sys.exit(1)
        
        # Initialize optimizer
        optimizer = BigQueryOptimizer(project_id=ctx.obj.get('project_id'))
        
        # Validate
        with console.status("[bold green]Validating queries..."):
            validation_result = optimizer.validate_optimization(
                original_query, optimized_query, sample_size
            )
        
        # Display results
        _display_validation_results(validation_result)
        
        # Exit with appropriate code
        if validation_result["overall_success"]:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('debug'):
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.option('--queries-file', '-f', type=click.Path(exists=True), required=True, 
              help='JSON file containing array of queries')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for results')
@click.option('--max-concurrent', type=int, default=3, help='Maximum concurrent optimizations')
@click.option('--validate/--no-validate', default=True, help='Validate query results')
@click.pass_context
def batch(ctx, queries_file: str, output_dir: Optional[str], max_concurrent: int, validate: bool):
    """Optimize multiple queries in batch."""
    
    try:
        # Load queries
        with open(queries_file, 'r') as f:
            queries_data = json.load(f)
        
        if isinstance(queries_data, list):
            queries = queries_data
        elif isinstance(queries_data, dict) and 'queries' in queries_data:
            queries = queries_data['queries']
        else:
            console.print("[red]Error: Invalid queries file format[/red]")
            sys.exit(1)
        
        console.print(f"[blue]Optimizing {len(queries)} queries in batch...[/blue]")
        
        # Initialize optimizer
        optimizer = BigQueryOptimizer(project_id=ctx.obj.get('project_id'))
        
        # Optimize queries
        with console.status("[bold green]Optimizing queries..."):
            results = optimizer.batch_optimize_queries(
                queries, validate_results=validate, max_concurrent=max_concurrent
            )
        
        # Save results
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            batch_results = {
                'total_queries': len(queries),
                'successful_optimizations': sum(1 for r in results if not r.validation_error),
                'results': [r.model_dump() for r in results]
            }
            
            with open(output_path / 'batch_results.json', 'w') as f:
                json.dump(batch_results, f, indent=2, default=str)
            
            console.print(f"[green]Batch results saved to {output_path}[/green]")
        
        # Display summary
        _display_batch_summary(results)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('debug'):
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Check system status and configuration."""
    
    try:
        settings = get_settings()
        
        # Create status table
        table = Table(title="BigQuery Optimizer Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details")
        
        # Check configuration
        table.add_row(
            "Configuration",
            "✓ OK" if settings.google_cloud_project and settings.gemini_api_key else "✗ Missing",
            f"Project: {settings.google_cloud_project or 'Not set'}"
        )
        
        # Test optimizer
        try:
            optimizer = BigQueryOptimizer(project_id=ctx.obj.get('project_id'))
            connection_ok = optimizer.test_connection()
            stats = optimizer.get_optimization_statistics()
            
            table.add_row(
                "BigQuery Connection",
                "✓ Connected" if connection_ok else "✗ Failed",
                f"Project: {stats.get('bigquery_project', 'Unknown')}"
            )
            
            table.add_row(
                "Documentation",
                "✓ Loaded",
                f"Chunks: {stats.get('documentation_chunks', 0)}, Patterns: {stats.get('available_patterns', 0)}"
            )
            
            table.add_row(
                "AI Model",
                "✓ Configured",
                f"Model: {settings.gemini_model}"
            )
            
        except Exception as e:
            table.add_row("System", "✗ Error", str(e))
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


def _display_optimization_text(result, output_file: Optional[str] = None):
    """Display optimization results in text format."""
    
    # Main panel with summary
    summary_text = f"""
[bold]Query Optimization Results[/bold]

Original Query Length: {len(result.original_query)} characters
Optimized Query Length: {len(result.optimized_query)} characters
Optimizations Applied: {result.total_optimizations}
Processing Time: {result.processing_time_seconds:.2f} seconds

Estimated Improvement: {result.estimated_improvement:.1%} if result.estimated_improvement else 'Unknown'
Results Identical: {'✓ Yes' if result.results_identical else '✗ No'}
"""
    
    if result.actual_improvement:
        summary_text += f"Actual Improvement: {result.actual_improvement:.1%}\n"
    
    console.print(Panel(summary_text, title="Summary", border_style="blue"))
    
    # Optimizations applied
    if result.optimizations_applied:
        table = Table(title="Optimizations Applied")
        table.add_column("Pattern", style="cyan")
        table.add_column("Description")
        table.add_column("Expected Improvement", style="green")
        
        for opt in result.optimizations_applied:
            improvement = f"{opt.expected_improvement:.1%}" if opt.expected_improvement else "Unknown"
            table.add_row(opt.pattern_name, opt.description, improvement)
        
        console.print(table)
    
    # Display optimized query
    console.print("\n[bold]Optimized Query:[/bold]")
    syntax = Syntax(result.optimized_query, "sql", theme="monokai", line_numbers=True)
    console.print(syntax)
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write(result.optimized_query)
        console.print(f"\n[green]Optimized query saved to {output_file}[/green]")
    
    # Show any errors
    if result.validation_error:
        console.print(f"\n[red]Validation Error: {result.validation_error}[/red]")


def _display_optimization_table(result):
    """Display optimization results in table format."""
    
    table = Table(title="Query Optimization Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Original Length", f"{len(result.original_query)} chars")
    table.add_row("Optimized Length", f"{len(result.optimized_query)} chars")
    table.add_row("Optimizations", str(result.total_optimizations))
    table.add_row("Processing Time", f"{result.processing_time_seconds:.2f}s")
    
    if result.estimated_improvement:
        table.add_row("Est. Improvement", f"{result.estimated_improvement:.1%}")
    
    if result.actual_improvement:
        table.add_row("Actual Improvement", f"{result.actual_improvement:.1%}")
    
    table.add_row("Results Identical", "✓ Yes" if result.results_identical else "✗ No")
    
    console.print(table)


def _display_query_analysis(analysis):
    """Display query analysis results."""
    
    # Analysis summary
    table = Table(title="Query Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Complexity", analysis.complexity.value)
    table.add_row("Tables", str(analysis.table_count))
    table.add_row("JOINs", str(analysis.join_count))
    table.add_row("Subqueries", str(analysis.subquery_count))
    table.add_row("Window Functions", str(analysis.window_function_count))
    table.add_row("Aggregations", str(analysis.aggregate_function_count))
    table.add_row("Has Partition Filter", "✓ Yes" if analysis.has_partition_filter else "✗ No")
    
    console.print(table)
    
    # Potential issues
    if analysis.potential_issues:
        console.print("\n[bold red]Potential Issues:[/bold red]")
        for issue in analysis.potential_issues:
            console.print(f"• {issue}")
    
    # Applicable patterns
    if analysis.applicable_patterns:
        console.print(f"\n[bold green]Applicable Optimization Patterns ({len(analysis.applicable_patterns)}):[/bold green]")
        for pattern in analysis.applicable_patterns:
            console.print(f"• {pattern}")


def _display_validation_results(validation_result):
    """Display validation results."""
    
    overall_success = validation_result["overall_success"]
    
    # Main status
    status_text = "✓ PASSED" if overall_success else "✗ FAILED"
    status_color = "green" if overall_success else "red"
    
    console.print(f"\n[bold {status_color}]Validation {status_text}[/bold {status_color}]")
    console.print(f"Summary: {validation_result['summary']}")
    
    # Results validation
    results_val = validation_result["results_validation"]
    console.print(f"\nResults Identical: {'✓ Yes' if results_val.get('identical') else '✗ No'}")
    
    if not results_val.get("identical") and "error" in results_val:
        console.print(f"[red]Error: {results_val['error']}[/red]")
    
    # Performance validation
    if "performance_validation" in validation_result:
        perf_val = validation_result["performance_validation"]
        if "improvement_percentage" in perf_val:
            improvement = perf_val["improvement_percentage"]
            console.print(f"Performance Improvement: {improvement:.1%}")


def _display_batch_summary(results):
    """Display batch optimization summary."""
    
    total = len(results)
    successful = sum(1 for r in results if not r.validation_error)
    failed = total - successful
    
    # Summary table
    table = Table(title="Batch Optimization Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")
    
    table.add_row("Total Queries", str(total))
    table.add_row("Successful", str(successful))
    table.add_row("Failed", str(failed))
    
    if successful > 0:
        avg_optimizations = sum(r.total_optimizations for r in results if not r.validation_error) / successful
        table.add_row("Avg Optimizations", f"{avg_optimizations:.1f}")
    
    console.print(table)


if __name__ == '__main__':
    cli()