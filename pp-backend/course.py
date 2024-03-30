class Course:
    def __init__(self, title, description, outcomes, restrictions, prereqs, department):
        self.title = title
        self.description = description
        self.outcomes = outcomes
        self.restrictions = restrictions
        self.prereqs = prereqs
        self.department = department
    
    def toString(self):
        return f"""The course {self.title} has the following prerequisite requirements: {self.prereqs}.
        The course description is: {self.description}. {self.title} is restricted to {self.restrictions}.
        {self.title} has the following expected outcomes: {self.outcomes}."""

    def findPostreqs(self):
        print("work in progress")