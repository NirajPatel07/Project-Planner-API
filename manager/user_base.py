from db.db_utility import get_session
from db.models import User, Team
import json
from datetime import datetime


class UserBase:
    def create_user(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            user_data = json.loads(request)

            # Extract the user details from the request
            name = user_data.get("name")
            display_name = user_data.get("display_name")

            # Create a new User instance
            user = User(name=name, display_name=display_name)

            # Add the user to the session and commit the transaction
            session.add(user)
            session.commit()

            # Return the JSON response with the created user's ID
            response = {"id": user.id}
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def list_users(self) -> str:
        session = get_session()

        try:
            # Query all users from the database
            users = session.query(User).all()

            # Prepare the response JSON
            response = [
                {
                    "name": user.name,
                    "display_name": user.display_name,
                    "creation_time": str(user.creation_time)
                }
                for user in users
            ]

            # Return the JSON response with the list of users
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def describe_user(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            user_data = json.loads(request)

            # Extract the user ID from the request
            user_id = user_data.get("id")

            # Query the user from the database
            user = session.query(User).filter_by(id=user_id).first()
            input_date = str(user.creation_time)
            input_date = input_date.split('.')[0]  # Remove milliseconds
            datetime_obj = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
            formatted_date = datetime_obj.strftime("%d %B %Y")

            if user:
                # Prepare the response JSON
                response = {
                    "name": user.name,
                    "description": f'{user.name} was created on {formatted_date}',
                    "creation_time": str(user.creation_time)
                }

                # Return the JSON response with the user details
                return json.dumps(response)
            else:
                # User not found, raise an exception or return an appropriate response
                raise ValueError("User not found")

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def update_user(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            update_data = json.loads(request)

            # Extract the user ID and updated user details from the request
            user_id = update_data.get("id")
            user_details = update_data.get("user", {})

            # Query the user from the database
            user = session.query(User).filter_by(id=user_id).first()

            if user:
                # Update the user details if provided in the request
                if "display_name" in user_details:
                    user.display_name = user_details["display_name"]

                # Commit the transaction
                session.commit()

                # Return a success message or appropriate response
                return "User updated successfully"
            else:
                # User not found, raise an exception or return an appropriate response
                raise ValueError("User not found")

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def get_user_teams(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            user_data = json.loads(request)

            # Extract the user ID from the request
            user_id = user_data.get("id")

            # Query the user from the database
            user = session.query(User).filter_by(id=user_id).first()

            if user:
                # Get the teams associated with the user
                teams = user.teams

                # Prepare the response JSON
                response = [
                    {
                        "name": team.name,
                        "description": team.description,
                        "creation_time": str(team.creation_time)
                    }
                    for team in teams
                ]

                # Return the JSON response with the list of teams
                return json.dumps(response)
            else:
                # User not found, raise an exception or return an appropriate response
                raise ValueError("User not found")

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()
