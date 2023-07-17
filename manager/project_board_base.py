from db.db_utility import get_session
from db.models import ProjectBoard, Task
import json
from datetime import datetime


class ProjectBoardBase:
    def create_board(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            board_data = json.loads(request)

            # Extract the board details from the request
            name = board_data.get("name")
            description = board_data.get("description")
            team_id = board_data.get("team_id")

            # Create a new ProjectBoard instance
            board = ProjectBoard(name=name, description=description, team_id=team_id)

            # Add the board to the session and commit the transaction
            session.add(board)
            session.commit()

            # Return the JSON response with the created board's ID
            response = {"id": board.id}
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def close_board(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            board_data = json.loads(request)

            # Extract the board ID from the request
            board_id = board_data.get("id")

            # Query the board from the database
            board = session.query(ProjectBoard).filter_by(id=board_id).first()

            if board:
                # Check if all tasks in the board are marked as COMPLETE
                if all(task.status == "COMPLETE" for task in board.tasks):
                    # Set the board status to CLOSED and record the end_time
                    board.closed = True
                    board.end_time = datetime.now()

                    # Commit the transaction
                    session.commit()

                    # Return a success message or appropriate response
                    return "Board closed successfully"
                else:
                    # Return an appropriate response indicating that the board cannot be closed
                    return "Cannot close the board. All tasks are not marked as complete."
            else:
                # Board not found, raise an exception or return an appropriate response
                raise ValueError("Board not found")

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def add_task(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            task_data = json.loads(request)

            # Extract the task details from the request
            title = task_data.get("title")
            description = task_data.get("description")
            user_id = task_data.get("user_id")
            board_id = task_data.get("board_id")

            # Create a new Task instance
            task = Task(title=title, description=description, user_id=user_id, board_id=board_id)

            # Add the task to the session and commit the transaction
            session.add(task)
            session.commit()

            # Return the JSON response with the created task's ID
            response = {"id": task.id}
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def update_task_status(self, request: str):
        session = get_session()

        try:
            # Parse the request JSON
            update_data = json.loads(request)

            # Extract the task ID and updated status from the request
            task_id = update_data.get("id")
            status = update_data.get("status")

            # Query the task from the database
            task = session.query(Task).filter_by(id=task_id).first()

            if task:
                # Update the task status
                task.status = status

                # Commit the transaction
                session.commit()

                # Return a success message or appropriate response
                return "Task status updated successfully"
            else:
                # Task not found, raise an exception or return an appropriate response
                raise ValueError("Task not found")

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def list_boards(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            team_data = json.loads(request)

            # Extract the team ID from the request
            team_id = team_data.get("id")

            # Query the boards for the team from the database
            boards = session.query(ProjectBoard).filter_by(team_id=team_id).all()

            # Prepare the response JSON
            response = [
                {
                    "id": board.id,
                    "name": board.name
                }
                for board in boards
            ]

            # Return the JSON response with the list of boards
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def export_board(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            board_data = json.loads(request)

            # Extract the board ID from the request
            board_id = board_data.get("id")

            # Query the board from the database
            board = session.query(ProjectBoard).filter_by(id=board_id).first()

            if board:
                # Generate the output file name
                out_file = f"out/board_{board_id}.txt"

                # Open the file in write mode and write the board details
                with open(out_file, "w") as file:
                    file.write(f"Board Name: {board.name}\n")
                    file.write(f"Board Description: {board.description}\n")
                    file.write("Tasks:\n")

                    board_tasks = session.query(Task).filter_by(board_id=board_id).all()
                    print('\n\n', board_tasks, '\n\n')
                    # Write the task details
                    if board_tasks:
                        for task in board_tasks:
                            file.write(f"- Title: {task.title if task.title else None}\n")
                            file.write(f"  Description: {task.description if task.description else None}\n")
                            file.write(f"  Status: {task.status if task.status else None}\n")
                            file.write(f"  Assigned User Id: {task.user_id if task.user_id else None}\n\n")\

                # Return the JSON response with the output file name
                response = {"out_file": out_file}
                return json.dumps(response)
            else:
                # Board not found, raise an exception or return an appropriate response
                raise ValueError("Board not found")

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()
