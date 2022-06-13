extern crate dotenv;

use dotenv::dotenv;
use notion::ids::DatabaseId;
use notion::NotionApi;
use serde::Deserialize;
use std::{error::Error, str::FromStr};
use teloxide::{prelude::*, utils::command::BotCommands};

#[tokio::main]
async fn main() {
    // load environment variables from .env
    dotenv().expect("Failed to read .env file");

    // parse environment variables into config struct
    let bot_config = envy::from_env::<BotConfig>().expect("Couldn't read bot config");

    // initialize logger
    pretty_env_logger::init();
    log::info!("Starting throw dice bot...");

    // create a Bot instance from token
    let bot = Bot::new(bot_config.telegram_bot_token);

    // create an instace of Notion API client
    let notion_api = NotionApi::new(bot_config.notion_api_token)
        .expect("Couldn't connect to Notion API with the provided token");

    let db = notion_api
        .get_database(
            DatabaseId::from_str(&*bot_config.finance_database_id)
                .expect("unable to parse database_id"),
        )
        .await
        .expect("Failed to get the database");

    println!("{:?}", db);

    // teloxide::repl(bot, |message: Message, bot: AutoSend<Bot>| async move {
    //     bot.send_dice(message.chat.id).await?;
    //     respond(())
    // })
    // .await;

    // teloxide::commands_repl(bot, answer, Command::ty()).await;
}

#[derive(Deserialize, Debug)]
struct BotConfig {
    telegram_bot_token: String,
    notion_api_token: String,
    finance_database_id: String,
}

#[derive(BotCommands, Clone)]
#[command(
    rename = "lowercase",
    description = "The following commands are supported"
)]
enum Command {
    #[command(description = "display this text.")]
    Help,
}

async fn answer(
    bot: AutoSend<Bot>,
    message: Message,
    command: Command,
) -> Result<(), Box<dyn Error + Send + Sync>> {
    match command {
        Command::Help => {
            bot.send_message(message.chat.id, Command::descriptions().to_string())
                .await?
        }
    };

    Ok(())
}
