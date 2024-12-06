class DiscountsUtil:

    def apply_discount(self, total_amount, total_purchase):
        if(total_purchase >= 5):
            return total_amount - ((total_amount * 0.20)/100)
        else:
            return total_amount
