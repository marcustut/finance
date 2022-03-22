package main

import (
	"context"
	"fmt"

	"github.com/jomei/notionapi"
	"github.com/kr/pretty"
	"github.com/marcustut/finance/config"
	"github.com/marcustut/finance/pkg/entity"
	"github.com/marcustut/finance/pkg/repository"
	"github.com/samber/lo"
)

func main() {
	// read config from env
	config.ReadConfig()

	client := notionapi.NewClient(notionapi.Token(config.C.Notion.IntegrationToken))

	repo := repository.NewExpenseRepository(client)

	es, err := repo.ListAll(context.TODO())
	if err != nil {
		panic(err)
	}

	lo.ForEach(es, func(e entity.Expense, i int) {
		fmt.Printf("%# v\n", pretty.Formatter(struct {
			entity.Expense
		}{
			Expense: entity.Expense{
				Name:     e.Name,
				Amount:   e.Amount,
				Comment:  e.Comment,
				Category: e.Category,
			},
		}))
	})
}
