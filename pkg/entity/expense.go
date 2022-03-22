package entity

import (
	"fmt"
	"time"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/pkg/entity/notion"
	"github.com/marcustut/finance/pkg/util/pointer"
)

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

// CreateExpenseInput represents a mutation input for creating an expense.
type CreateExpenseInput struct {
	Name     string
	Amount   float64
	Date     time.Time
	Comment  string
	Category ExpenseCategory
}

// NotionProperties returns the corresponding notion properties object for CreateExpenseInput.
func (i *CreateExpenseInput) NotionProperties() notionapi.Properties {
	return map[string]notionapi.Property{
		string(notion.FinancePropertyName): notionapi.TitleProperty{
			Title: []notionapi.RichText{
				{
					Text: notionapi.Text{
						Content: i.Name,
					},
				},
			},
		},
		string(notion.FinancePropertyAmount): notionapi.NumberProperty{
			Number: i.Amount,
		},
		string(notion.FinancePropertyDate): notionapi.DateProperty{
			Date: notionapi.DateObject{
				Start: (*notionapi.Date)(pointer.Time(i.Date)),
			},
		},
		string(notion.FinancePropertyComment): notionapi.RichTextProperty{
			RichText: []notionapi.RichText{
				{
					Text: notionapi.Text{
						Content: i.Comment,
					},
				},
			},
		},
		string(notion.FinancePropertyCategoryExpense): notionapi.SelectProperty{
			Select: notionapi.Option{
				Name: string(i.Category),
			},
		},
	}
}

// MapToExpense maps a finance notion page to an expense.
func MapToExpense(page notionapi.Page) (*Expense, error) {
	var expense Expense

	name, ok := page.Properties[string(notion.FinancePropertyName)].(*notionapi.TitleProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as TitleProperty", notion.FinancePropertyName)
	}
	if len(name.Title) == 0 {
		expense.Name = ""
	} else {
		expense.Name = name.Title[0].PlainText
	}

	amount, ok := page.Properties[string(notion.FinancePropertyAmount)].(*notionapi.NumberProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as NumberProperty", notion.FinancePropertyAmount)
	}
	expense.Amount = amount.Number

	category, ok := page.Properties[string(notion.FinancePropertyCategoryExpense)].(*notionapi.SelectProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as SelectProperty", notion.FinancePropertyCategoryExpense)
	}
	expense.Category = ExpenseCategory(category.Select.Name)

	date, ok := page.Properties[string(notion.FinancePropertyDate)].(*notionapi.DateProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as DateProperty", notion.FinancePropertyDate)
	}
	expense.Date.Start = (*time.Time)(date.Date.Start)
	expense.Date.End = (*time.Time)(date.Date.End)

	comment, ok := page.Properties[string(notion.FinancePropertyComment)].(*notionapi.RichTextProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as RichTextProperty", notion.FinancePropertyComment)
	}
	if len(comment.RichText) == 0 {
		expense.Comment = ""
	} else {
		expense.Comment = comment.RichText[0].PlainText
	}

	return &expense, nil
}

// MapToExpenses maps an array of finance notion pages to an array of expenses.
func MapToExpenses(pages []notionapi.Page) ([]Expense, error) {
	es := make([]Expense, len(pages))
	for i, page := range pages {
		e, err := MapToExpense(page)
		if err != nil {
			return nil, err
		}
		es[i] = *e
	}
	return es, nil
}
