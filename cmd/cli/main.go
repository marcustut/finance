package main

import (
	"fmt"
	"log"
	"os"

	"github.com/jomei/notionapi"
	"github.com/marcustut/finance/config"
	"github.com/marcustut/finance/pkg/registry"
	"github.com/marcustut/finance/pkg/repository"
	"github.com/urfave/cli/v2"
)

// ListFlags represents the flags for list command.
type ListFlags struct {
	Type string
}

func init() {
	// read config from env
	config.ReadConfig()
}

func main() {
	client := notionapi.NewClient(notionapi.Token(config.C.Notion.IntegrationToken))
	r := registry.NewRegistry(repository.NewExpenseRepository(client), repository.NewIncomeRepository(client))

	// init flags
	lflags := new(ListFlags)

	app := &cli.App{
		Name:  "finance",
		Usage: "manage incomes and expenses",
		Commands: []*cli.Command{
			{
				Name:    "list",
				Aliases: []string{"l"},
				Usage:   "list all incomes or finances",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:        "type",
						Aliases:     []string{"t"},
						Usage:       "type of finance object to display (either 'income' or 'expense')",
						Required:    true,
						Destination: &lflags.Type,
					},
				},
				Action: func(ctx *cli.Context) error {
					// validate type
					if lflags.Type != "income" && lflags.Type != "expense" {
						return fmt.Errorf("type must be either 'income' or 'expense'")
					}

					// handle list
					switch lflags.Type {
					case "income":
						is, err := r.Income.ListAll(ctx.Context)
						if err != nil {
							return err
						}
						fmt.Printf("%#v", is)
					case "expense":
						es, err := r.Expense.ListAll(ctx.Context)
						if err != nil {
							return err
						}
						fmt.Printf("%#v", es)
					}

					return nil
				},
			},
		},
	}

	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}
