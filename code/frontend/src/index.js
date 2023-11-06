import React from "react";
import ReactDOM from "react-dom";
import { ReactiveBase } from "@appbaseio/reactivesearch";
import GoodreadsSearch from "./GoodreadsSearch";

ReactDOM.render(
  <React.StrictMode>
      <GoodreadsSearch />
  </React.StrictMode>,
  document.getElementById("root")
);
