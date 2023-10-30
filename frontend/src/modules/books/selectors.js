const getModuleState = state => state.books;

export const getBooks = state => getModuleState(state).books;