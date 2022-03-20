package config

import (
	"log"
	"os"
	"path"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/joho/godotenv"
	"github.com/spf13/viper"
)

type config struct {
	Notion struct {
		IntegrationToken string `mapstructure:"integration_token"`
		DatabaseIDs      struct {
			Finance string
		} `mapstructure:"database_ids"`
	}
}

// C is a global config variable.
var C config

// ReadConfig reads from config file and initialize C.
func ReadConfig() {
	cwd := filepath.Join(rootDir(), "config")
	viper.AddConfigPath(cwd)

	// load config
	viper.SetConfigName("/config")
	if err := godotenv.Load(cwd + "/.env"); err != nil {
		log.Fatal("error loading .env file: ", err)
	}

	viper.SetConfigType("yml")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		log.Fatal("error reading config: ", err)
	}

	// replace env in yml with environment variables
	for _, k := range viper.AllKeys() {
		val := viper.GetString(k)
		if strings.HasPrefix(val, "${") && strings.HasSuffix(val, "}") {
			viper.Set(k, getEnvOrPanic(strings.TrimSuffix(strings.TrimPrefix(val, "${"), "}")))
		}
	}

	if err := viper.Unmarshal(&C); err != nil {
		log.Print("error unmarshaling config: ", err)
		os.Exit(1)
	}
}

func rootDir() string {
	_, b, _, _ := runtime.Caller(0)
	d := path.Join(path.Dir(b))
	return filepath.Dir(d)
}

func getEnvOrPanic(envKey string) string {
	env := os.Getenv(envKey)
	if len(env) == 0 {
		panic("unable to find " + envKey + " in the environment")
	}
	return env
}
