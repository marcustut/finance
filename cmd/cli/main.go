package main

import (
	"context"
	"fmt"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/config"
	"github.com/marcustut/finance/pkg/repository"
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

	fmt.Printf("%#v\n", es)
}
