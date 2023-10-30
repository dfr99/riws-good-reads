import * as actionTypes from './actionTypes';
import backend from '../../backend';

export const getBooks = (title, author, rating, summary, genres, release_date,
    number_of_pages, isbn, language, cover_page) => dispatch => {
        backend.elastic.crearRequest(title, author, rating, summary, genres, release_date,
            number_of_pages, isbn, language, cover_page,
            result => dispatch(getBooksCompleted(result.hits.hits)));
    }

export const getBooksCompleted = (books) => ({
    type: actionTypes.GET_BOOKS_COMPLETED,
    books
})