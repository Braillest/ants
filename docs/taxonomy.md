# Ants

Ants is Braillest's a distributed system for braille transcription, mold generation, and management.

# Roles

## Queen

The queen orchestrates the entire process and provides the backbone for the system.
Creates compute tasks for workers to perform.
Creates I/O tasks for drones to perform.
Provides:
- Redis for fast cache.
- File storage.
- Database for metadata about file storage.
- RabbitMQ message queue for task distribution.

## Worker

Performs compute tasks assigned by the queen.
Runs celery worker instances to perform compute tasks.

Operations:
- Transcribing documents to braille
- Generating diffs between transcriptions and back translations
- Generating molds

## Drone

Performs I/O tasks assigned by the queen.
Runs celery worker instances to perform I/O tasks.

Operations:
- Cleaning redis
- Moving files around
- Deleting files

# Example

1. Queen receives a document to be converted into braille molds.
2. Queen creates I/O tasks for drones to move the document into redis in preperation for the workers.
- Queen puts the document in local file storage.
- Queen creates I/O tasks for drones to move the document into redis, serialize it to remove offending characters and generate a diff to denote the performed changes, translate it to braille, backtranslate it to text and generate a diff to denote the performed changes, format the braille to the specified format (eg braillest standard), paginate the braille, back translate the paginated braille for the possibility of dual modality books, and puts everything needed for mold generation into redis. Finally, notifying the queen of completion.
3. Queen creates compute tasks for the workers to perform.
4. Workers recieve the tasks, performs them, and notifies the queen of completion.
- Mold generation is computationally expensive, 1/s. Results are stored in redis.
5. Queen creates I/O tasks for drones to move data out of redis and into file storage.
- Queen provides a database for metadata about file storage. Drones perform I/O metadata calculation and inserts records into the queens database and file storage.
6. Queen creates I/O task for drone to create a github repo and pushes files from the queens file storage into the github repo.
