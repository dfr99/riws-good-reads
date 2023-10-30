import { combineReducers } from "redux";

import app from "../modules/app";
import books from "../modules/books";

const rootReducer = () =>
  combineReducers({
    app: app.reducer,
    books: books.reducer
  });

export default rootReducer;