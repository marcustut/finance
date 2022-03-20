package entity

import "time"

// ExpenseCategory is the possible category that an expense falls under.
type ExpenseCategory string

const (
	// ExpenseCategoryTransport is a type of ExpenseCategory.
	ExpenseCategoryTransport ExpenseCategory = "Transport"
	// ExpenseCategoryEducation is a type of ExpenseCategory.
	ExpenseCategoryEducation ExpenseCategory = "Education"
	// ExpenseCategorySubscription is a type of ExpenseCategory.
	ExpenseCategorySubscription ExpenseCategory = "Subscription"
	// ExpenseCategoryEntertainment is a type of ExpenseCategory.
	ExpenseCategoryEntertainment ExpenseCategory = "Entertainment"
	// ExpenseCategoryFood is a type of ExpenseCategory.
	ExpenseCategoryFood ExpenseCategory = "Food"
)

// Expense represents a money spent on certain stuff.
type Expense struct {
	Name   string
	Amount float64
	Date   struct {
		Start *time.Time
		End   *time.Time
	}
	Comment  string
	Category ExpenseCategory
}
