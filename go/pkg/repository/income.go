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

// IncomeRepository supports CRUD operations for Income.
type IncomeRepository struct {
	client *notionapi.Client
}

// NewIncomeRepository constructs the repository.
func NewIncomeRepository(client *notionapi.Client) *IncomeRepository {
	return &IncomeRepository{client}
}

// ListAll fetches all incomes.
func (r *IncomeRepository) ListAll(ctx context.Context) ([]entity.Income, error) {
	var results []notionapi.Page

	// construct query param
	dqr := &notionapi.DatabaseQueryRequest{
		PropertyFilter: &notionapi.PropertyFilter{
			Property: string(notion.FinancePropertyAmount),
			Number: &notionapi.NumberFilterCondition{
				GreaterThan: pointer.Float64(0),
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

	// UniqBy removes the duplicated page and MapToIncomes convert it to Income entity
	es, err := entity.MapToIncomes(lo.UniqBy(results, func(p notionapi.Page) notionapi.ObjectID { return p.ID }))
	if err != nil {
		return nil, err
	}

	return es, nil
}

// List fetches a list of incomes.
func (r *IncomeRepository) List(ctx context.Context, cursor *notionapi.Cursor, pageSize *int, sorts []notionapi.SortObject) ([]entity.Income, error) {
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

	// map to Income entity
	es, err := entity.MapToIncomes(db.Results)
	if err != nil {
		return nil, err
	}

	return es, nil
}

// Create adds an income.
func (r *IncomeRepository) Create(ctx context.Context, input entity.CreateIncomeInput) (*entity.Income, error) {
	// amount must be positive
	if input.Amount <= 0 {
		return nil, fmt.Errorf("amount for an income must be greater than 0")
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

	// map to Income entity
	e, err := entity.MapToIncome(*res)
	if err != nil {
		return nil, err
	}

	return e, nil
}
