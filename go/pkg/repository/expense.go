package repository

import (
	"context"
	"fmt"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/config"
	"github.com/marcustut/finance/pkg/entity"
	"github.com/marcustut/finance/pkg/entity/notion"
	"github.com/marcustut/finance/pkg/util/pointer"
	"github.com/samber/lo"
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
	var results []notionapi.Page

	// construct query param
	dqr := &notionapi.DatabaseQueryRequest{
		PropertyFilter: &notionapi.PropertyFilter{
			Property: string(notion.FinancePropertyAmount),
			Number: &notionapi.NumberFilterCondition{
				LessThanOrEqualTo: pointer.Float64(0),
			},
		},
	}

	// query for the database
	resp, err := r.client.Database.Query(ctx, notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance), dqr)
	if err != nil {
		return nil, err
	}
	results = append(results, resp.Results...)

	// keep fetching if there's more
	for resp.HasMore {
		dqr.StartCursor = notionapi.Cursor(results[len(results)-1].ID)
		resp, err = r.client.Database.Query(ctx, notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance), dqr)
		if err != nil {
			return nil, err
		}
		results = append(results, resp.Results...)
	}

	// UniqBy removes the duplicated page and MapToExpenses convert it to expense entity
	es, err := entity.MapToExpenses(lo.UniqBy(results, func(p notionapi.Page) notionapi.ObjectID { return p.ID }))
	if err != nil {
		return nil, err
	}

	return es, nil
}

// List fetches a list of expenses.
func (r *ExpenseRepository) List(ctx context.Context, cursor *notionapi.Cursor, pageSize *int, sorts []notionapi.SortObject) ([]entity.Expense, error) {
	// construct the query param
	dqr := &notionapi.DatabaseQueryRequest{
		PropertyFilter: &notionapi.PropertyFilter{
			Property: "Amount",
			Number: &notionapi.NumberFilterCondition{
				LessThanOrEqualTo: pointer.Float64(0),
			},
		},
		Sorts: sorts,
	}
	if cursor != nil {
		dqr.StartCursor = *cursor
	}
	if pageSize != nil {
		dqr.PageSize = *pageSize
	}

	// query the db
	db, err := r.client.Database.Query(ctx, notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance), dqr)
	if err != nil {
		return nil, err
	}

	// map to expense entity
	es, err := entity.MapToExpenses(db.Results)
	if err != nil {
		return nil, err
	}

	return es, nil
}

// Create adds an expense.
func (r *ExpenseRepository) Create(ctx context.Context, input entity.CreateExpenseInput) (*entity.Expense, error) {
	// amount must be negative
	if input.Amount > 0 {
		return nil, fmt.Errorf("amount for an expense must be 0 or lesser")
	}

	// create a finance record
	res, err := r.client.Page.Create(ctx, &notionapi.PageCreateRequest{
		Parent: notionapi.Parent{
			DatabaseID: notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance),
		},
		Properties: input.NotionProperties(),
	})
	if err != nil {
		return nil, err
	}

	// map to expense entity
	e, err := entity.MapToExpense(*res)
	if err != nil {
		return nil, err
	}

	return e, nil
}
