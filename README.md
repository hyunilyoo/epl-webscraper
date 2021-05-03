# EPL-Webscraper
## How to use
### Crawler for Club statistics
- Use `clubstats_spider.py` in `clubstats_crawler/spiders/`
- e.g. `scapy crawl Clubstats`  

This will get every club statistics for every season such as:  
```
1. club_name
2. goal_per_match
3. shot_on_target
4. shooting_accuracy
5. big_chance_created
6. pass_per_game
7. cross
8. cross_accuracy
9. goal_conceded_per_match
10. tackle_success
11. clearance
12. aerial_battles
13. interceptions
14. season
```
### Crawler for Table info 
- Use `tables_spider.py` in `tables_crawler/spiders/`
- e.g. `scapy crawl Tables`  

This will get every club statistics for every season such as:  
```
1. club_name 
2. position 
3. won
4. lost 
5. drawn
6. goal
7. goal_against 
8. points 
```
### Crawler for players' statistics
In Progress...