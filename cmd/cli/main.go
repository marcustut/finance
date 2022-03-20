package main

import (
	"context"
	"fmt"

	"github.com/jomei/notionapi"
	"github.com/kr/pretty"
	"github.com/marcustut/finance/config"
	"github.com/samber/lo"
)

func main() {
	// read config from env
	config.ReadConfig()

	client := notionapi.NewClient(notionapi.Token(config.C.Notion.IntegrationToken))

	db, err := client.Database.Query(context.Background(), notionapi.DatabaseID(config.C.Notion.DatabaseIDs.Finance), nil)
	if err != nil {
		panic(err)
	}

	results := lo.Map(db.Results, func(page notionapi.Page, _ int) notionapi.Page {
		return page
	})

	fmt.Printf("%# v\n", pretty.Formatter(results))
}
