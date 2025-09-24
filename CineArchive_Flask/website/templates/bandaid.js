    // === Show/Hide Search Popup ===
    function openSearch() {
      document.getElementById('search-popup')?.classList.remove('hidden');
    }

    function closeSearch() {
      document.getElementById('search-popup')?.classList.add('hidden');
    }

    // === Navigate to Movie Details Page ===
    function redirectToMoviePage(movieId) {
      window.location.href = `movie.html?id=${movieId}`;
    }

    // === Handle Search Button Click ===
    function handleSearchClick() {
      const raw = document.getElementById('searchInput').value.trim();
      const { title, year, person } = parseSearchInput(raw);
      fetchSearchResults(title, year, person);
    }

    // === Listen to Input Field Live Changes ===
    document.getElementById('searchInput').addEventListener('input', function () {
      const raw = this.value.trim();
      const { title, year, person } = parseSearchInput(raw);

      if (title || year || person) {
        fetchSearchResults(title, year, person);
      } else {
        document.getElementById('search-results').innerHTML = '';
      }
    });

    // === Extract Title, Year, and Person Name ===
    function parseSearchInput(raw) {
      const yearMatch = raw.match(/\b(19|20)\d{2}\b/);
      const year = yearMatch ? yearMatch[0] : '';
      const cleanedInput = year ? raw.replace(year, '').trim() : raw;

      const personMatch = cleanedInput.match(/^[a-zA-Z\s]+$/);
      const person = personMatch && cleanedInput.split(' ').length >= 2 ? cleanedInput : '';
      const title = person ? '' : cleanedInput;

      return { title, year, person };
    }

    // === Fetch and Display Search Results from TMDb ===
    async function fetchSearchResults(title = '', year = '', person = '') {
      const token = 'yJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjBmZTI2MTRkNDQ3ZTFjNDAwMDBkNmJjYTQwYTZiOCIsIm5iZiI6MS43NDY5MDAzNjQ5ODU5OTk4ZSs5LCJzdWIiOiI2ODFmOTU4Y2QzMzJiZTY0NjRhMTU5Y2UiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.v5oNBG3nwHQkjO4hl62MiH58CLwLHc-3R3ECa2DbyKE';
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json;charset=utf-8'
      };

      const seen = new Set();
      let movieResults = [];

      try {
        if (person) {
          const personUrl = `https://api.themoviedb.org/3/search/person?query=${encodeURIComponent(person)}&include_adult=false&language=en-US&page=1`;
          const personRes = await fetch(personUrl, { headers });
          const personData = await personRes.json();

          if (personData.results?.length > 0) {
            const knownMovies = personData.results
              .flatMap(p => p.known_for)
              .filter(m => m.media_type === 'movie');

            const filtered = year
              ? knownMovies.filter(m => m.release_date?.startsWith(year))
              : knownMovies;

            movieResults.push(...filtered);
          }
        }

        if (title) {
          const movieUrl = `https://api.themoviedb.org/3/search/movie?query=${encodeURIComponent(title)}${year ? `&year=${year}` : ''}`;
          const movieRes = await fetch(movieUrl, { headers });
          const movieData = await movieRes.json();

          if (movieData.results) {
            movieResults.push(...movieData.results);
          }
        }

        const uniqueMovies = movieResults.filter(movie => {
          if (!seen.has(movie.id)) {
            seen.add(movie.id);
            return true;
          }
          return false;
        });

        for (const movie of uniqueMovies) {
          const genreUrl = `https://api.themoviedb.org/3/movie/${movie.id}?language=en-US`;
          const genreRes = await fetch(genreUrl, { headers });
          const genreData = await genreRes.json();
          movie.genres = genreData.genres;
        }

        let resultsHtml = '';
        if (uniqueMovies.length > 0) {
          uniqueMovies.forEach(movie => {
            const genres = movie.genres ? movie.genres.map(g => g.name).join(', ') : 'No Genre';
            if (movie.poster_path) {
              resultsHtml += `
                <div class="search-result-item" onclick="redirectToMoviePage('${movie.id}')">
                  <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}" />
                  <span>${movie.title} (${movie.release_date ? movie.release_date.split('-')[0] : ''})</span>
                </div>`;
            }
          });
        } else {
          resultsHtml = '<p>No results found.</p>';
        }

        document.getElementById('search-results').innerHTML = resultsHtml;

      } catch (err) {
        console.error('Error fetching search results:', err);
        document.getElementById('search-results').innerHTML = '<p>There was an error fetching the results.</p>';
      }
    }

    // === Fetching Popular Movies for Slideshow ===
    const token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjBmZTI2MTRkNDQ3ZTFjNDAwMDBkNmJjYTQwYTZiOCIsIm5iZiI6MS43NDY5MDAzNjQ5ODU5OTk4ZSs5LCJzdWIiOiI2ODFmOTU4Y2QzMzJiZTY0NjRhMTU5Y2UiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.v5oNBG3nwHQkjO4hl62MiH58CLwLHc-3R3ECa2DbyKE';
    fetch('https://api.themoviedb.org/3/movie/popular?language=en-US&page=1', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json;charset=utf-8'
      }
    })
    .then(response => response.json())
    .then(async data => {
      const movies = data.results.slice(0, 5);
      const slideshow = document.getElementById('slideshow');

      for (const movie of movies) {
        const imagesResponse = await fetch(`https://api.themoviedb.org/3/movie/${movie.id}/images`, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json;charset=utf-8'
          }
        });

        const imagesData = await imagesResponse.json();
        const backdropPath = movie.backdrop_path ? `https://image.tmdb.org/t/p/w1280${movie.backdrop_path}` : '';

        const slide = document.createElement('div');
        slide.className = 'slide';
        slide.innerHTML = `
          <div class="slide-image">
            <img src="${backdropPath}" alt="${movie.title}" />
          </div>`;
        slideshow.appendChild(slide);
      }

      let currentSlide = 0;
      const slides = document.querySelectorAll('.slide');
      if (slides.length > 0) slides[0].style.display = 'block';

      setInterval(() => {
        slides[currentSlide].style.display = 'none';
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].style.display = 'block';
      }, 4000);
    })
    .catch(error => {
      console.error('Error loading slideshow:', error);
    });