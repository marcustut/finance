package entity

import (
	"fmt"
	"time"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/pkg/entity/notion"
	"github.com/marcustut/finance/pkg/util/pointer"
)

// IncomeCategory is the possible category that an income falls under.
type IncomeCategory string

const (
	// IncomeCategoryWork is a type of IncomeCategory.
	IncomeCategoryWork IncomeCategory = "Work"
	// IncomeCategoryParent is a type of IncomeCategory.
	IncomeCategoryParent IncomeCategory = "Parent"
	// IncomeCategoryClaim is a type of IncomeCategory.
	IncomeCategoryClaim IncomeCategory = "Claim"
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

// CreateIncomeInput represents a mutation input for creating an input.
type CreateIncomeInput struct {
	Name     string
	Amount   float64
	Date     time.Time
	Comment  string
	Category IncomeCategory
}

// NotionProperties returns the corresponding notion properties object for CreateIncomeInput.
func (i *CreateIncomeInput) NotionProperties() notionapi.Properties {
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
		string(notion.FinancePropertyCategoryIncome): notionapi.SelectProperty{
			Select: notionapi.Option{
				Name: string(i.Category),
			},
		},
	}
}

// MapToIncome maps a finance notion page to an income.
func MapToIncome(page notionapi.Page) (*Income, error) {
	var income Income

	name, ok := page.Properties[string(notion.FinancePropertyName)].(*notionapi.TitleProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as TitleProperty", notion.FinancePropertyName)
	}
	if len(name.Title) == 0 {
		income.Name = ""
	} else {
		income.Name = name.Title[0].PlainText
	}

	amount, ok := page.Properties[string(notion.FinancePropertyAmount)].(*notionapi.NumberProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as NumberProperty", notion.FinancePropertyAmount)
	}
	income.Amount = amount.Number

	category, ok := page.Properties[string(notion.FinancePropertyCategoryIncome)].(*notionapi.SelectProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as SelectProperty", notion.FinancePropertyCategoryIncome)
	}
	income.Category = IncomeCategory(category.Select.Name)

	date, ok := page.Properties[string(notion.FinancePropertyDate)].(*notionapi.DateProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as DateProperty", notion.FinancePropertyDate)
	}
	income.Date.Start = (*time.Time)(date.Date.Start)
	income.Date.End = (*time.Time)(date.Date.End)

	comment, ok := page.Properties[string(notion.FinancePropertyComment)].(*notionapi.RichTextProperty)
	if !ok {
		return nil, fmt.Errorf("unable to cast '%s' property of finance as RichTextProperty", notion.FinancePropertyComment)
	}
	if len(comment.RichText) == 0 {
		income.Comment = ""
	} else {
		income.Comment = comment.RichText[0].PlainText
	}

	return &income, nil
}

// MapToIncomes maps an array of finance notion pages to an array of incomes.
func MapToIncomes(pages []notionapi.Page) ([]Income, error) {
	is := make([]Income, len(pages))
	for idx, page := range pages {
		i, err := MapToIncome(page)
		if err != nil {
			return nil, err
		}
		is[idx] = *i
	}
	return is, nil
}
