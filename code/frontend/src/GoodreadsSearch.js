

import React, { useState } from 'react';
import {
    ReactiveBase,
    DataSearch,
    SingleList,
    DateRange,
    ReactiveList,
    ResultCard,
    SingleRange,
} from "@appbaseio/reactivesearch";
import "./GoodreadsSearch.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar, faCalendar } from "@fortawesome/free-solid-svg-icons";

const GoodreadsSearch = () => {
    const [showRatingFilter, setRatingFilter] = useState(false);
    const [dateRange, setDateRange] = useState(null);
    const [showDateFilter, setDateFilter] = useState(false);
    return (
        <ReactiveBase
            app="good_reads"
            url="http://localhost:9200"
        >
            <div>
                <div className="toolbar">
                    <div className="title">RIWS Good Reads</div>
                    <DataSearch
                        componentId="textSearch"
                        dataField={["title", "author"]}
                        placeholder="Buscar por título o autor"
                        URLParams={true}
                    />
                    <button
                        className="filter-button"
                        onClick={() => setRatingFilter(!showRatingFilter)}
                    >
                        <FontAwesomeIcon icon={faStar} className="star-icon" />
                    </button>
                    <button
                        className="filter-button"
                        onClick={() => setDateFilter(!showDateFilter)}
                    >
                        <FontAwesomeIcon icon={faCalendar} className="calendar-icon" />
                    </button>
                </div>
            </div>
            {showRatingFilter && (
                <div className="rating-filter">
                    <SingleRange
                        componentId="ratingFilter"
                        dataField="average_rating"
                        title="Puntuación media"
                        data={[
                            { label: "1 - 2 ⭐", start: 1, end: 2 },
                            { label: "2 - 3 ⭐", start: 2, end: 3 },
                            { label: "3 - 4 ⭐", start: 3, end: 4 },
                            { label: "4 - 5 ⭐", start: 4, end: 5 },
                        ]}
                        URLParams={true}
                    />
                </div>
            )}
            {showDateFilter && (
                <div className="date-range-container">
                    <DateRange
                        defaultValue={{
                            start: new Date('2017-04-01'),
                            end: new Date('2017-04-07'),
                        }}
                        componentId="dateRange"
                        dataField="release_date"
                        title="Filtrar por fecha"
                        queryFormat="date"
                        URLParams={true}
                        onChange={value => setDateRange(value)}
                    />
                </div>
            )}
            <ReactiveList
                componentId="resultsList"
                dataField="title"
                size={10}
                pagination={true}
                react={{ "and": ["textSearch", "ratingFilter", "dateRange"] }}
                renderResultStats={(stats) => (
                    <div>{stats.numberOfResults} resultados encontrados</div>
                )}
                renderItem={(data) => (
                    <ResultCard key={data._id}>
                        <ResultCard.Image src={data.image_url} />
                        <ResultCard.Title>
                            <div dangerouslySetInnerHTML={{ __html: data.title }} />
                        </ResultCard.Title>
                        <ResultCard.Description>
                            <div>
                                Author: {data.author} <br />
                                Average Rating: {data.average_rating} <br />
                                Publication Year: {data.original_publication_year}
                            </div>
                        </ResultCard.Description>
                    </ResultCard>
                )}
            />
        </ReactiveBase >
    );
};

export default GoodreadsSearch;

