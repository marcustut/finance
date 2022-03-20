package repository

import (
	"context"
	"fmt"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/config"
	"github.com/marcustut/finance/pkg/entity"
	"github.com/marcustut/finance/pkg/entity/notion"
)

// ExpenseRepository supports CRUD operations for Expense.
type ExpenseRepository struct {
	client *notionapi.Client
}

// NewExpenseRepository constructs the repository.
func NewExpenseRepository(client *notionapi.Client) *ExpenseRepository {
	return &ExpenseRepository{client}
}

// ListAll fetches all expenses.
func (r *ExpenseRepository) ListAll(ctx context.Context) ([]entity.Expense, error) {
	// TODO: Update 'ListAll' to fetch all finances
	db, err := r.client.Database.Query(ctx, notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance), &notionapi.DatabaseQueryRequest{
		PropertyFilter: &notionapi.PropertyFilter{
			Property: string(notion.FinancePropertyAmount),
			Number: &notionapi.NumberFilterCondition{
				// LessThan and LessThanOrEqualTo not working
				LessThanOrEqualTo: 0,
			},
		},
	})
	if err != nil {
		return nil, err
	}
	fmt.Println(len(db.Results))

	es, err := notion.MapToExpenses(db.Results)
	if err != nil {
		return nil, err
	}

	return es, nil
}

// List fetches a list of expenses.
func (r *ExpenseRepository) List(ctx context.Context) ([]entity.Expense, error) {
	// TODO: Update 'List' to support pagination
	db, err := r.client.Database.Query(ctx, notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance), &notionapi.DatabaseQueryRequest{
		PropertyFilter: &notionapi.PropertyFilter{
			Property: "Amount",
			Number: &notionapi.NumberFilterCondition{
				LessThanOrEqualTo: 0,
			},
		},
	})
	if err != nil {
		return nil, err
	}

	es, err := notion.MapToExpenses(db.Results)
	if err != nil {
		return nil, err
	}

	return es, nil
}
