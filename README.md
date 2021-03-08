# airflow-gui
A new look to airflow graphical user interface

## Run locally in docker
Make sure that you have airflow service running locally and update [/api/app.py](/api/app.py) services to point to the right adress.
```
docker-compose up
```


## A short summary of how it is created:
* Python Flask application dealing with modifying and providing the dag-graphs
* Graphql server that provides information from airflow database such as dagruns and statuses
* A vue webservice which mostly relies on vuetify material plate for rendering in the custom theme I created as well as ReteJS for the node programming tool which is very epic!
* The flask service also requires an running instance of airflow and that you provide authentication CSRF tokens to it to use the API to for example trigger/clear tasks or add connections

## Feature list:
* List and filter dags based on status and dagname
* List and filter connections based on name
* Show dag information such as dagruns and status on each run and for each task in the dag.
* Trigger a new dagrun
* Modify tasks and dependencies
* Add additional tasks and dependencies
* Remove tasks and dependencies
* Use logic nodes to create a computed value input to a dag (not stored at current state of developement)
* Save all modifications

## Uppcomming features
* Show gant/time durations in a chart for each dagrun in a graph
* Pause/resume a dag
* Modify dag params like schedule time, dag name catchup etc.
* Add fresh and new dags
* Mark task/dag as failed (e.g. stop running dagrun)
