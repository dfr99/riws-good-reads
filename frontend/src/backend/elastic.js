import {config, appFetch} from "./appFetch";

export const crearRequest = (title, author, rating, summary, genres, release_date, 
    number_of_pages, isbn,language, cover_page,onSuccess) =>
    appFetch(`/reviews`,
    config("POST", {critica: {title, author, rating, summary, genres, release_date, 
        number_of_pages, isbn, language, cover_page}}),onSuccess);
