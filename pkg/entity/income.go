package entity

import "time"

// IncomeCategory is the possible category that an income falls under.
type IncomeCategory string

const (
	// ExpenseCategoryWork is a type of IncomeCategory.
	ExpenseCategoryWork IncomeCategory = "Work"
	// ExpenseCategoryParent is a type of IncomeCategory.
	ExpenseCategoryParent IncomeCategory = "Parent"
	// ExpenseCategoryClaim is a type of IncomeCategory.
	ExpenseCategoryClaim IncomeCategory = "Claim"
)

// Income represents an amount of money received from a certain source.
type Income struct {
	Name   string
	Amount float64
	Date   struct {
		Start *time.Time
		End   *time.Time
	}
	Comment  string
	Category IncomeCategory
}
