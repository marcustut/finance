extern crate dotenv;

use dotenv::dotenv;
use std::error::Error;
use teloxide::{prelude::*, utils::command::BotCommands};

#[tokio::main]
async fn main() {
    // load environment variables from .env
    dotenv().ok();

    pretty_env_logger::init();
    log::info!("Starting throw dice bot...");

    let bot = Bot::from_env().auto_send();

    // teloxide::repl(bot, |message: Message, bot: AutoSend<Bot>| async move {
    //     bot.send_dice(message.chat.id).await?;
    //     respond(())
    // })
    // .await;

    teloxide::commands_repl(bot, answer, Command::ty()).await;
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
