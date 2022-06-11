package registry

import "github.com/marcustut/finance/pkg/repository"

// Registry is a for injecting dependencies.
type Registry struct {
	Expense *repository.ExpenseRepository
	Income  *repository.IncomeRepository
}

// NewRegistry construct an instance of Registry.
func NewRegistry(expenseRepo *repository.ExpenseRepository, incomeRepo *repository.IncomeRepository) *Registry {
	return &Registry{expenseRepo, incomeRepo}
}
