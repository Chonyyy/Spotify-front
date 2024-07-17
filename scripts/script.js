$(document).ready(function () {
    const apiUrl = 'http://localhost:8001/songs';
    let audioElement = $('<audio>', { id: 'audio-player', controls: false }).appendTo('body')[0];
    let currentPage = 1;
    const pageSize = 4;   

    function fetchSongs(page) {
        axios.get(apiUrl, { params: { limit: pageSize, offset: (page - 1) * pageSize } })
            .then(response => {
                const songs = response.data;
                const musicList = $('.music-list .items');
                musicList.empty();  // Limpia los elementos existentes

                if (songs.length === 0) {
                    musicList.append('<p>No songs found</p>');
                    return;
                }

                songs.forEach((song, index) => {
                    // Crea el HTML para cada canción
                    const songItem = `
                        <div class="item" data-song-id="${song.id}" data-song-title="${song.title}" data-song-artist="${song.artist}" data-song-image="${song.img}" data-song-url="${song.address}">
                            <div class="info">
                                <p>${index + 1}</p>
                                <img src="${song.img}" alt="${song.title}">
                                <div class="details">
                                    <h5>${song.title}</h5>
                                    <p>${song.artist}</p>
                                </div>
                            </div>
                            <div class="actions">
                                <p>03:45</p> <!-- Aquí podrías agregar la duración de la canción si la tienes -->
                                <div class="icon">
                                    <i class='bx bxs-right-arrow'></i>
                                </div>
                                <i class='bx bxs-plus-square' id="download-${song.id}" style="cursor: pointer;"></i>
                            </div>
                        </div>
                    `;
                    musicList.append(songItem);
                });

                // Agrega el manejador de eventos para actualizar el reproductor al hacer clic en una canción
                $('.music-list .item').on('click', function () {
                    const songId = $(this).data('song-id');
                    const songTitle = $(this).data('song-title');
                    const songArtist = $(this).data('song-artist');
                    const songUrl = $(this).data('song-url');
                    const songImage = $(this).data('song-image');

                    updatePlayer(songId, songTitle, songArtist, songImage, songUrl);
                });

                // Agrega el manejador de eventos para descargar la canción al hacer clic en el ícono
                $('.music-list .bxs-plus-square').on('click', function () {
                    const songItem = $(this).closest('.item');
                    const songUrl = songItem.data('song-url');
                    downloadSong(songUrl);
                });

                // Actualiza el estado de los botones de paginación
                $('#prev-page').toggleClass('disabled', page === 1);
                $('#next-page').toggleClass('disabled', songs.length < pageSize);
                $('#page-info').text(`Page ${page}`);

            })
            .catch(error => {
                console.error('Error fetching songs:', error);
            });
    }

    function updatePlayer(songId, songTitle, songArtist, songImage, songUrl) {
        // Actualiza la información del reproductor
        $('.music-player .song-info img').attr('src', songImage);
        $('.music-player .description h3').text(songTitle);
        $('.music-player .description h5').text(songArtist);
        $('.music-player .description p').text('Best of 2024');

        const url = `${apiUrl}/stream/${encodeURIComponent(songTitle)}`;
        const audioElement = document.getElementById('audio-player');
        audioElement.src = url
        audioElement.play()

        // Actualiza el progreso de la canción
        setInterval(updateProgress, 1000);

        // Botones de control
        $('#play-btn').on('click', function () {
            if (audioElement.paused) {
                audioElement.play();
                $(this).removeClass('bx bxs-right-arrow').addClass('bx bxs-pause');
            } else {
                audioElement.pause();
                $(this).removeClass('bx bxs-pause').addClass('bx bxs-right-arrow');
            }
        });

        $('#prev-btn').on('click', function () {
            // Implementar funcionalidad para la canción anterior
        });

        $('#next-btn').on('click', function () {
            // Implementar funcionalidad para la siguiente canción
        });

        $('#repeat-btn').on('click', function () {
            audioElement.loop = !audioElement.loop;
            $(this).toggleClass('active', audioElement.loop);
        });

        $('#shuffle-btn').on('click', function () {
            // Implementar funcionalidad para reproducir aleatoriamente
        });

        $('#lyrics-btn').on('click', function () {
            // Implementar funcionalidad para mostrar las letras de la canción
        });
    }

    function updateProgress() {
        if (audioElement.duration) {
            const progress = (audioElement.currentTime / audioElement.duration) * 100;
            $('.progress .active-line').css('width', `${progress}%`);
            $('.progress p').first().text(formatTime(audioElement.currentTime));
            $('.progress p').last().text(formatTime(audioElement.duration));
        }
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    function fetchSongSearch(query = '') {
        const url = `${apiUrl}/${encodeURIComponent(query)}`;
        axios.get(url)
            .then(response => {
                const song = response.data;
                const musicList = $('.music-list .items');
                musicList.empty();  // Limpia los elementos existentes

                if (!song) {
                    musicList.append('<p>No song found</p>');
                    return;
                }

                const songItem = `
                    <div class="item" data-song-id="${song.id}" data-song-title="${song.title}" data-song-artist="${song.artist}" data-song-image="${song.img}" data-song-url="${song.address}">
                        <div class="info">
                            <p>1</p>
                            <img src="${song.img}">
                            <div class="details">
                                <h5>${song.title}</h5>
                                <p>${song.artist}</p>
                            </div>
                        </div>
                        <div class="actions">
                            <p>03:45</p>
                            <div class="icon">
                                <i class='bx bxs-right-arrow'></i>
                            </div>
                            <i class='bx bxs-plus-square' id="download-${song.id}" style="cursor: pointer;"></i>
                        </div>
                    </div>
                `;
                musicList.append(songItem);

                // Agrega el manejador de eventos para actualizar el reproductor al hacer clic en la canción encontrada
                $('.music-list .item').on('click', function () {
                    const songId = $(this).data('song-id');
                    const songTitle = $(this).data('song-title');
                    const songArtist = $(this).data('song-artist');
                    const songImage = $(this).data('song-image');
                    const songUrl = $(this).data('song-url');

                    updatePlayer(songId, songTitle, songArtist, songImage, songUrl);
                });

                // Agrega el manejador de eventos para descargar la canción al hacer clic en el ícono
                $('.music-list .bxs-plus-square').on('click', function () {
                    const songItem = $(this).closest('.item');
                    const songUrl = songItem.data('song-url');
                    downloadSong(songUrl);
                });
            })
            .catch(error => {
                console.error('Error fetching song:', error);
                $('.music-list .items').empty().append('<p>Error fetching song</p>');
            });
    }

    function fetchSongsByGenre(genre, page) { //TODO: Arreglar esto
        const url = `${apiUrl}/genre/${encodeURIComponent(genre)}`;
        axios.get(url, { params: { limit: pageSize, offset: (page - 1) * pageSize } })
            .then(response => {
                const songs = response.data;
                const musicList = $('.music-list .items');
                musicList.empty();  // Limpia los elementos existentes

                if (songs.length === 0) {
                    musicList.append('<p>No songs found for the genre</p>');
                    return;
                }

                songs.forEach((song, index) => {
                    const songItem = `
                        <div class="item" data-song-id="${song.id}" data-song-title="${song.title}" data-song-artist="${song.artist}" data-song-image="${song.img}" data-song-url="${song.address}">
                            <div class="info">
                                <p>${index + 1}</p>
                                <img src="${song.img}" alt="${song.title}">
                                <div class="details">
                                    <h5>${song.title}</h5>
                                    <p>${song.artist}</p>
                                </div>
                            </div>
                            <div class="actions">
                                <p>03:45</p> <!-- Aquí podrías agregar la duración de la canción si la tienes -->
                                <div class="icon">
                                    <i class='bx bxs-right-arrow'></i>
                                </div>
                                <i class='bx bxs-plus-square' id="download-${song.id}" style="cursor: pointer;"></i>
                            </div>
                        </div>
                    `;
                    musicList.append(songItem);
                });

                // Agrega el manejador de eventos para actualizar el reproductor al hacer clic en una canción
                $('.music-list .item').on('click', function () {
                    const songId = $(this).data('song-id');
                    const songTitle = $(this).data('song-title');
                    const songArtist = $(this).data('song-artist');
                    const songImage = $(this).data('song-image');
                    const songUrl = $(this).data('song-url');

                    updatePlayer(songId, songTitle, songArtist, songImage, songUrl);
                });

                // Agrega el manejador de eventos para descargar la canción al hacer clic en el ícono
                $('.music-list .bxs-plus-square').on('click', function () {
                    const songItem = $(this).closest('.item');
                    const songUrl = songItem.data('song-url');
                    downloadSong(songUrl);
                });
            })
            .catch(error => {
                console.error('Error fetching songs by genre:', error);
                $('.music-list .items').empty().append('<p>Error fetching songs</p>');
            });
    }

    function downloadSong(url) {
        const link = document.createElement('a');
        link.href = url;
        link.download = url.split('/').pop(); // Usa el nombre del archivo como nombre para la descarga
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    $('.search button').on('click', function () {
        const query = $('#search-input').val();
        fetchSongSearch(query);
    });

    // Agrega el manejador de eventos para los elementos de género
    $('.genres .item').on('click', function () {
        const genre = $(this).text().trim();
        currentPage = 1
        fetchSongsByGenre(genre,currentPage);
    });

    $('.genres .header').on('click', function () {
        currentPage = 1
        fetchSongs(currentPage);
    });

    // Manejo de eventos de paginación
    $('#prev-page').on('click', function () {
        if (currentPage > 1) {
            currentPage--;
            fetchSongs(currentPage);
        }
    });

    $('#next-page').on('click', function () {
        currentPage++;
        fetchSongs(currentPage);
    });

    // Inicializar la primera página
    fetchSongs(currentPage);
});
