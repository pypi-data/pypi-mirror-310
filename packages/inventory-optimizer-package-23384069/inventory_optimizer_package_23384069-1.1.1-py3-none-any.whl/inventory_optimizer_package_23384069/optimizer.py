class InventoryOptimizer:
    def __init__(self, min_stock_threshold=10):
        self.min_stock_threshold = min_stock_threshold
        self.period = 7

    def calculate_weekly_average(self, product_id, order_item_model):
        """Calculate 7-day average sales from delivered orders"""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Sum

        end_date = timezone.now()
        start_date = end_date - timedelta(days=self.period)

        # Get sales quantity from delivered orders in last 7 days
        sales = order_item_model.objects.filter(
            product_id=product_id,
            order__status="DELIVERED",  # Only count delivered orders
            order__order_date__range=(start_date, end_date)
        ).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0

        daily_average = abs(sales) / self.period
        return daily_average

    def generate_recommendations(self, product_id, order_item_model, current_stock):
        daily_average = self.calculate_weekly_average(
            product_id, 
            order_item_model
        )
        
        reorder_point = daily_average * 3  # 3 days supply
        
        return {
            'product_id': product_id,
            'current_stock': current_stock,
            'daily_average_usage': daily_average,
            'reorder_point': reorder_point,
            'recommended_order': daily_average * 7,  # 7 days supply
            'needs_reorder': current_stock <= reorder_point
        }