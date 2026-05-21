rm(list = ls())
install.packages("tidyr")
install.packages("shiny")
install.packages("shinylive")
install.packages("rsconnect")
library("ggplot2")
library("tidyr")
library("shiny")

chess_data <- read_csv("chess_data.csv")
may_opponents <- read_csv("opponents_2026_05.csv")

chess_data <- data.frame(
  Format = c("Blitz", "Rapid"),
  Current_Rating = c(334, 624),
  Best_Rating = c(448, 624),
  Wins = c(115, 112),
  Losses = c(105, 84),
  Draws = c(2, 10)
)

record_long <- pivot_longer(chess_data, 
                            cols = c(Wins, Losses, Draws), 
                            names_to = "Outcome", 
                            values_to = "Games")

ui <- fluidPage(
  titlePanel("Chess Analytics"),
  
  mainPanel(
    plotOutput("graph"),
    plotOutput("scatter")
  )
)

server <- function(input, output) {
  output$graph <- renderPlot({
    ggplot(record_long, aes(x = Format, y = Games, fill = Outcome)) +
      geom_bar(stat = "identity", position = "dodge") +
      theme_minimal() +
      labs(title = "Game Outcomes: Blitz vs Rapid",
           x = "Time Format",
           y = "Number of Games",
           fill = "Outcome")
  }) 
  output$scatter <- renderPlot({
    ggplot(data = opponents_2026_05, aes(x = Date, y = Opponent_Rating, color = Time_Format)) + geom_point() + theme_minimal() +
      labs(title = "Opponent Ratings over Time (May 2026)",
           x = "Date",
           y = "Opponent Elo Rating",
           color = "Format")
  }) 
}

shinyApp(ui = ui, server = server)

