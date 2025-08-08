class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance
    
    def transfer(self, amount, destination_category):
        if self.check_funds(amount):
            # Add withdrawal to source category
            self.withdraw(amount, f"Transfer to {destination_category.name}")
            # Add deposit to destination category
            destination_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __str__(self):
        # Title line - 30 characters with category name centered
        title_line = self.name.center(30, "*")
        
        # Ledger items
        ledger_lines = []
        for item in self.ledger:
            # First 23 characters of description
            description = item["description"][:23]
            # Format amount to 2 decimal places, right-aligned in 7 characters
            amount_str = f"{item['amount']:.2f}"
            # Combine description and amount, total line should be 30 characters
            line = f"{description:<23}{amount_str:>7}"
            ledger_lines.append(line)
        
        # Total line
        total = self.get_balance()
        total_line = f"Total: {total:.2f}"
        
        # Combine all parts
        result = [title_line] + ledger_lines + [total_line]
        return "\n".join(result)


def create_spend_chart(categories):
    # Calculate total withdrawals for each category
    category_withdrawals = []
    total_spent = 0
    
    for category in categories:
        withdrawals = 0
        for item in category.ledger:
            if item["amount"] < 0:  # Only count withdrawals (negative amounts)
                withdrawals += abs(item["amount"])
        category_withdrawals.append(withdrawals)
        total_spent += withdrawals
    
    # Calculate percentages and round down to nearest 10
    percentages = []
    for withdrawal in category_withdrawals:
        if total_spent > 0:
            percentage = (withdrawal / total_spent) * 100
            rounded_percentage = int(percentage // 10) * 10
        else:
            rounded_percentage = 0
        percentages.append(rounded_percentage)
    
    # Build the chart
    chart_lines = []
    
    # Title
    chart_lines.append("Percentage spent by category")
    
    # Y-axis labels and bars (from 100 to 0)
    for i in range(100, -10, -10):
        line = f"{i:>3}|"
        for percentage in percentages:
            if percentage >= i:
                line += " o "
            else:
                line += "   "
        line += " "  # Two extra spaces after final bar
        chart_lines.append(line)
    
    # Horizontal line below bars
    horizontal_line = "    " + "-" * (len(categories) * 3 + 1)
    chart_lines.append(horizontal_line)
    
    # Category names written vertically
    max_name_length = max(len(category.name) for category in categories) if categories else 0
    
    for i in range(max_name_length):
        line = "    "  # 4 spaces to align with the bars
        for category in categories:
            if i < len(category.name):
                line += f" {category.name[i]} "
            else:
                line += "   "
        line += " "  # Two extra spaces after final category
        chart_lines.append(line)
    
    return "\n".join(chart_lines)


# Example usage:
if __name__ == "__main__":
    food = Category('Food')
    food.deposit(1000, 'initial deposit')
    food.withdraw(10.15, 'groceries')
    food.withdraw(15.89, 'restaurant and more food for dessert')
    clothing = Category('Clothing')
    food.transfer(50, clothing)
    print(food)
    print()
    
    # Test the spend chart
    auto = Category('Auto')
    auto.deposit(1000, 'initial deposit')
    auto.withdraw(15)
    
    food_chart = Category('Food')
    food_chart.deposit(900, 'deposit')
    food_chart.withdraw(105.55)
    
    clothing_chart = Category('Clothing')
    clothing_chart.deposit(900, 'deposit')
    clothing_chart.withdraw(33.40)
    
    print(create_spend_chart([food_chart, clothing_chart, auto]))