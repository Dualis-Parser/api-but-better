# Dualis API

## Requirements
Should be able to return all modules and it's grades for a specific user from dualis.dhbw.de.
This should work for any grade and probably store the grades in a specified data structure but due to dualis' incompetence that may be impossible.

### Email notifications
Additional any user who wants to should get an email if a grade has been updated.

## Routes
### GET /api/user

**Request**
```json
{
  "username": "surname.lastname@domain",
  "password": "password"
}
```

**Response**
```json
{
  "code": 200,
  "data": {
    "username": "surname.lastname@domain",
    "name": "Surname Lastname",
    "modules": [
      {
        "module_no": "",
        "module_name": "",
        "final_grade": "",
        "credits": "",
        "exams_url": "",
        "passed": false,
        "semesters": "",
        "grades": "html table content"
      }
    ]
  }
}
```