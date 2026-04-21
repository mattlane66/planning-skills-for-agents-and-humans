# Brownfield Admin Search — Current Notes

The current admin page already works for browsing users.

Today:
- users can land on the admin page
- they can scroll through the list
- they can click a row to open a user detail page
- when they go back, they return to the list page

Problems:
- when the list is long, finding one user is slow
- admins often know part of a name or email but cannot search
- the team wants search, but does not want to break the current browse flow

Early ideas:
- maybe add a search input at the top
- maybe persist the query in the URL
- maybe debounce search input

Constraints:
- keep the current row click → detail page behavior
- do not remove basic browsing
- keep the first version small
