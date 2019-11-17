# Ticket to Ride Simulation Engine ![DOI](https://zenodo.org/badge/215415182.svg)
### By R. Teal Witter

Adapted from Fernando de Silva's [work](https://github.com/fernandomsilva/Ticket-to-Ride-Engine/).

## Modifications to the Simulation
1. Run `game_object.setup()` to set up the game.
2. Return dictionary of routes and Destination Tickets from `printScoring` method.
3. Prevent agents from buying the same double-route (some cities have two routes between them) twice in four-player games
by changing the `get_free_connections` method.

## Additional Features
1. Run simulations of two-player and four-player games and store the results, Destination Tickets, and routes for each game.
2. Generate figures of the proportion of wins by Destination Tickets and claims per game of routes.
