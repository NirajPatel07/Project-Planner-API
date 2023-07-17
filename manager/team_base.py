from db.db_utility import get_session
from db.models import Team, User
import json


class TeamBase:
    def create_team(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            team_data = json.loads(request)

            # Extract the team details from the request
            name = team_data.get("name")
            description = team_data.get("description")
            admin_id = team_data.get("admin")

            # Create a new Team instance
            team = Team(name=name, description=description, admin_id=admin_id)

            # Add the team to the session and commit the transaction
            session.add(team)
            session.commit()

            # Return the JSON response with the created team's ID
            response = {"id": team.id}
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def list_teams(self) -> str:
        session = get_session()

        try:
            # Query all teams from the database
            teams = session.query(Team).all()

            # Prepare the response JSON
            response = [
                {
                    "name": team.name,
                    "description": team.description,
                    "creation_time": str(team.creation_time),
                    "admin": team.admin_id
                }
                for team in teams
            ]

            # Return the JSON response with the list of teams
            return json.dumps(response)

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def describe_team(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            team_data = json.loads(request)

            # Extract the team ID from the request
            team_id = team_data.get("id")

            # Query the team from the database
            team = session.query(Team).filter_by(id=team_id).first()

            if team:
                # Prepare the response JSON
                response = {
                    "name": team.name,
                    "description": team.description,
                    "creation_time": str(team.creation_time),
                    "admin": team.admin_id
                }

                # Return the JSON response with the team details
                return json.dumps(response)
            else:
                # Team not found, raise an exception or return an appropriate response
                raise ValueError("Team not found")

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def update_team(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            update_data = json.loads(request)

            # Extract the team ID and updated team details from the request
            team_id = update_data.get("id")
            team_details = update_data.get("team", {})

            # Query the team from the database
            team = session.query(Team).filter_by(id=team_id).first()

            if team:
                # Update the team details if provided in the request
                if "name" in team_details:
                    team.name = team_details["name"]
                if "description" in team_details:
                    team.description = team_details["description"]
                if "admin" in team_details:
                    team.admin_id = team_details["admin"]

                # Commit the transaction
                session.commit()

                # Return a success message or appropriate response
                return "Team updated successfully"
            else:
                # Team not found, raise an exception or return an appropriate response
                raise ValueError("Team not found")

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def add_users_to_team(self, request: str):
        session = get_session()

        try:
            # Parse the request JSON
            update_data = json.loads(request)

            # Extract the team ID and user IDs to add from the request
            team_id = update_data.get("id")
            user_ids = update_data.get("users", [])

            # Query the team from the database
            team = session.query(Team).filter_by(id=team_id).first()

            if team:
                # Query the users to add from the database
                users = session.query(User).filter(User.id.in_(user_ids)).all()

                # Add the users to the team
                team.members.extend(users)

                # Commit the transaction
                session.commit()

                # Return a success message or appropriate response
                return "Users added to the team successfully"
            else:
                # Team not found, raise an exception or return an appropriate response
                raise ValueError("Team not found")

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def remove_users_from_team(self, request: str):
        session = get_session()

        try:
            # Parse the request JSON
            update_data = json.loads(request)

            # Extract the team ID and user IDs to remove from the request
            team_id = update_data.get("id")
            user_ids = update_data.get("users", [])

            # Query the team from the database
            team = session.query(Team).filter_by(id=team_id).first()

            if team:
                # Query the users to remove from the database
                users = session.query(User).filter(User.id.in_(user_ids)).all()

                # Remove the users from the team
                team.members = [user for user in team.members if user not in users]

                # Commit the transaction
                session.commit()

                # Return a success message or appropriate response
                return "Users removed from the team successfully"
            else:
                # Team not found, raise an exception or return an appropriate response
                raise ValueError("Team not found")

        except Exception as e:
            # Handle any exceptions and rollback the transaction
            session.rollback()
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()

    def list_team_users(self, request: str) -> str:
        session = get_session()

        try:
            # Parse the request JSON
            team_data = json.loads(request)

            # Extract the team ID from the request
            team_id = team_data.get("id")

            # Query the team from the database
            team = session.query(Team).filter_by(id=team_id).first()

            if team:
                # Get the users associated with the team
                users = team.members

                # Prepare the response JSON
                response = [
                    {
                        "id": user.id,
                        "name": user.name,
                        "display_name": user.display_name
                    }
                    for user in users
                ]

                # Return the JSON response with the list of team users
                return json.dumps(response)
            else:
                # Team not found, raise an exception or return an appropriate response
                raise ValueError("Team not found")

        except Exception as e:
            # Handle any exceptions
            # Optionally, log the error or perform error handling
            raise e

        finally:
            # Close the session
            session.close()
