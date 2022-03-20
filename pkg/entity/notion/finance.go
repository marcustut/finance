package notion

import (
	"fmt"
	"time"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/pkg/entity"
)

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

// MapToExpense maps a finance notion page to an expense.
func MapToExpense(page notionapi.Page) (*entity.Expense, error) {
	var expense entity.Expense

	name, ok := page.Properties[string(FinancePropertyName)].(*notionapi.TitleProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as TitleProperty", FinancePropertyName)
	}
	if len(name.Title) == 0 {
		expense.Name = ""
	} else {
		expense.Name = name.Title[0].PlainText
	}

	amount, ok := page.Properties[string(FinancePropertyAmount)].(*notionapi.NumberProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as NumberProperty", FinancePropertyAmount)
	}
	expense.Amount = amount.Number

	category, ok := page.Properties[string(FinancePropertyCategoryExpense)].(*notionapi.SelectProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as SelectProperty", FinancePropertyCategoryExpense)
	}
	expense.Category = entity.ExpenseCategory(category.Select.Name)

	date, ok := page.Properties[string(FinancePropertyDate)].(*notionapi.DateProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as DateProperty", FinancePropertyDate)
	}
	expense.Date.Start = (*time.Time)(date.Date.Start)
	expense.Date.End = (*time.Time)(date.Date.End)

	comment, ok := page.Properties[string(FinancePropertyComment)].(*notionapi.RichTextProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as RichTextProperty", FinancePropertyComment)
	}
	if len(comment.RichText) == 0 {
		expense.Comment = ""
	} else {
		expense.Comment = comment.RichText[0].PlainText
	}

	return &expense, nil
}

// MapToExpenses maps an array of finance notion pages to an array of expenses.
func MapToExpenses(pages []notionapi.Page) ([]entity.Expense, error) {
	es := make([]entity.Expense, len(pages))
	for i, page := range pages {
		e, err := MapToExpense(page)
		if err != nil {
			return nil, err
		}
		es[i] = *e
	}
	return es, nil
}

// MapToIncome maps a finance notion page to an income.
func MapToIncome(page notionapi.Page) entity.Income {
	return entity.Income{}
}
