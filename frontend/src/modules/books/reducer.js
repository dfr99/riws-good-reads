import {combineReducers} from 'redux';

import * as actionTypes from './actionTypes';

const initialState = {
    books: []
};

const books = (state = initialState.books, action) => {

    switch (action.type) {

        case actionTypes.GET_BOOKS_COMPLETED:
            return action.books;

        default:
            return state;

    }

}


const reducer = combineReducers({
    books
});

export default reducer;