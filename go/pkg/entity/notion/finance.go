package notion

// FinanceProperty represents the property names of a finance notion page.
type FinanceProperty string

const (
	// FinancePropertyName is a type of FinanceProperty.
	FinancePropertyName FinanceProperty = "Name"
	// FinancePropertyAmount is a type of FinanceProperty.
	FinancePropertyAmount FinanceProperty = "Amount"
	// FinancePropertyCategoryExpense is a type of FinanceProperty.
	FinancePropertyCategoryExpense FinanceProperty = "Category (Expense)"
	// FinancePropertyCategoryIncome is a type of FinanceProperty.
	FinancePropertyCategoryIncome FinanceProperty = "Category (Income)"
	// FinancePropertyDate is a type of FinanceProperty.
	FinancePropertyDate FinanceProperty = "Date"
	// FinancePropertyComment is a type of FinanceProperty.
	FinancePropertyComment FinanceProperty = "Comment"
)
