(Content omitted)

    def test_window_with_case_when(self):
        """Test 10: Window function with CASE WHEN."""
        query = """
        SELECT customer_id,
               SUM(CASE WHEN status = 'completed' THEN total_amount ELSE 0 END) 
               OVER (PARTITION BY customer_id ORDER BY order_date) as running_total
        FROM orders
        """
        result = self.optimizer.optimize_query(query, validate_results=False)
        
        assert result.total_optimizations >= 1