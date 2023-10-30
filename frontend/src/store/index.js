import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";

import rootReducer from "./rootReducer";

const configureAppStore = () => {

  return configureStore({
    reducer: rootReducer(),
    middleware: [...getDefaultMiddleware()],
  });
};

export default configureAppStore;