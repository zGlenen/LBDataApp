# {% extends 'base.html' %}

# {% block head %}
#   <title>Films Wrapped - Films</title>
#   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
#   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>

# {% endblock %}

# {% block body %}

# <div class="text-center">
#   <div class="dropdown">
#     <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton2" data-bs-toggle="dropdown" aria-expanded="false">
#       Sort
#     </button>
#     <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton2">
#       <li><a class="dropdown-item" href="?sorting_option=year_latest">Year Latest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=year_earliest">Year Earliest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=rating_highest">Rating Highest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=rating_lowest">Rating Lowest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=user_rating_highest">User Rating Highest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=user_rating_lowest">User Rating Lowest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=longest">Longest</a></li>
#       <li><a class="dropdown-item" href="?sorting_option=shortest">Shortest</a></li>

#     </ul>
#   </div>
#   <div class="dropdown">
#     <button class="btn btn-secondary dropdown-toggle" type="button" id="ratingDropdown" data-bs-toggle="dropdown" aria-expanded="false">
#       Your Rating
#     </button>
#     <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton2" id="ratingDropdownMenu">
    #   <li><a class="dropdown-item" href="?rating_option=0">Not Rated</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=1">½</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=2">★</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=3">★½</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=4">★★</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=5">★★½</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=6">★★★</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=7">★★★½</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=8">★★★★</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=9">★★★★½</a></li>
    #   <li><a class="dropdown-item" href="?rating_option=10">★★★★★</a></li>
#     </ul>
#   </div>
#   <div class="dropdown">
#     <button class="btn btn-secondary dropdown-toggle" type="button" id="ratingDropdown" data-bs-toggle="dropdown" aria-expanded="false">
#       Avg. Rating
#     </button>
#     <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton2" id="ratingDropdownMenu">
    #   <li><a class="dropdown-item" href="?avg_rating_option=0">Not Rated</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=0.5">0.5</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=1.0">1.0</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=1.5">1.5</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=2.0">2</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=2.5">2.5</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=3.0">3</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=3.5">3.5</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=4.0">4</a></li>
    #   <li><a class="dropdown-item" href="?avg_rating_option=4.5">4.5</a></li>
#     </ul>
#   </div>
#   <div class="row">
#       <div class="col-sm-8">

#       </div>
#       <div class="col-sm-4">

#       </div>
#   </div>

#   <table class="table table-dark table-sm w-auto mx-auto">
#       <thead>
#           <tr>
#               <th scope="col">Title</th>
#               <th scope="col">Your Rating</th>
#               <th scope="col">Release Year</th>
#               <th scope="col">Runtime</th>
#               <th scope="col">Director</th>
#               <th scope="col">Poster</th>
#               <th scope="col">Average Rating</th>
#           </tr>
#       </thead>
#       <tbody>
#           {% for film in films %}
#           <tr>
#               <td class="align-middle">{{ film.title }}</td>
#               <td class="align-middle">{{ film.details.user_rating }}</td>
#               <td class="align-middle">{{ film.year_released }}</td>
#               <td class="align-middle">{{ film.details.runtime }}</td>
#               <td class="align-middle">
#                   {% set director_count = 0 %}
#                   {% for crew_member in film.details.crew %}
#                       {% if crew_member.job == 'Director' %}
#                           {% if director_count > 0 %}, {% endif %}
#                           {{ crew_member.name }}
#                           {% set director_count = director_count + 1 %}
#                       {% endif %}
#                   {% endfor %}
#               </td>
#               <td class="align-middle"><a href="{{ film.letterboxd_uri }}"><img style="max-height: 100px;" src="https://image.tmdb.org/t/p/original/{{ film.details.image_url }}"></a></td>
#               <td class="align-middle">{{ film.details.rating }}</td>

#           </tr>
#           {% endfor %}
#           <!-- Pagination -->

#       </tbody>
#   </table>
#   <div class="text-center">
#     <ul class="pagination justify-content-center">
#         {{ pagination.links }}
#     </ul>
#     {{ pagination.info }}

#   </div>
# </div>
# <script>
  
#   document.getElementById('navbar').style.display = 'block';

# </script>
   
# {% endblock %}
