

import React from 'react';
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
const { ResultCardsWrapper } = ReactiveList;
const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const formattedDate = new Date(dateString).toLocaleDateString('es-ES', options);
    return formattedDate;
};

const handleToggleFilter = (componentId, value) => {
    const currentSelected = ReactiveBase.getComponent(componentId).defaultSelected;

    const updatedSelected = currentSelected === value ? null : value;

    ReactiveBase.updateComponent(componentId, {
      defaultSelected: updatedSelected,
    });
    ReactiveBase.triggerDefaultQuery();
  };

  const CustomResultCard = ({ data }) => (
    <div className="custom-result-card">
       <div className="cover-image-container">
      <div
        className="cover-image"
        style={{ backgroundImage: `url(${data.cover_page})` }}
      ></div>
    </div>
      <div className="card-content">
        <ResultCard.Title>
          <div dangerouslySetInnerHTML={{ __html: data.title }} />
        </ResultCard.Title>
        <ResultCard.Description>
          <div>
            Autor/a: {data.author} <br />
            Puntuación media: {parseFloat(data.number_of_pages)} <br />
            Fecha de publicación: {formatDate(data.release_date)} <br />
            Sinopsis: {data.summary} <br />
            Géneros: {data.genres.join(", ")} <br /> 
            Número de páginas: {parseInt(data.number_of_pages)} <br />
            ISBN: {data.isbn} <br />
            Idioma: {data.language}
          </div>
        </ResultCard.Description>
      </div>
    </div>
  );
  

const GoodreadsSearch = () => {
    return (

        <ReactiveBase
            app="good_reads"
            url="http://localhost:9200"
        >
            <div>
                <div className="toolbar">
                    <div className="title">RIWS Good Reads</div>
                    <div className="text-search">
                        <DataSearch
                            componentId="textSearch"
                            dataField={["title", "author"]}
                            placeholder="Buscar por título o autor"
                            URLParams={true}
                        />
                    </div>
                </div>
            </div>
            <div className="app-container">
                <div className="filters-container">
                    <div className='filters-title'>Filtros</div>
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
                    <div className="pages-filter">
                        <SingleRange
                            componentId="pagesFilter"
                            dataField="number_of_pages"
                            title="Número de páginas"
                            data={[
                                { label: " < 100", start: 1, end: 100 },
                                { label: "100 - 300", start: 100, end: 300 },
                                { label: "300 - 500", start: 300, end: 500 },
                                { label: "500 - 700", start: 500, end: 700 },
                                { label: "700 - 1000", start: 700, end: 1000 },
                                { label: " > 1000", start: 1000, end: 10000 },
                            ]}
                            URLParams={true}
                            showFilter={true}
                            defaultSelected={null} 
                            renderItem={(label, count, isSelected) => (
                              <div
                                key={label}
                                onClick={() => handleToggleFilter("pagesFilter", label)}
                                className={`option ${isSelected ? "selected" : ""}`}
                              >
                                {label}
                              </div>
                            )}
                        />
                    </div>
                    <div className="date-range-container">
                        <DateRange
                            componentId="dateRange"
                            dataField="release_date"
                            title="Fcha de publicación"
                            customQuery={(value, props) => {
                                const start = value && value.start ? new Date(value.start).toISOString().split('T')[0] : null;
                                const end = value && value.end ? new Date(value.end).toISOString().split('T')[0] : null;

                                return {
                                    range: {
                                        [props.dataField]: {
                                            gte: start,
                                            lte: end,
                                        },
                                    },
                                };
                            }}
                            placeholder={{ start: "Fecha de inicio", end: "Fecha de fin" }}
                        />
                    </div>
                </div>
                <div className="results-container">
                    <ReactiveList style={{ width: '100%' }}
                        componentId="SearchResult"
                        dataField="title"
                        size={3}
                        pagination={true}
                        react={{ "and": ["textSearch", "ratingFilter", "dateRange"] }}
                        renderResultStats={(stats) => (
                            <div>{stats.numberOfResults} resultados encontrados</div>
                        )}>
                        {({ data, error, loading }) => (
                            <ResultCardsWrapper style={{ width: '100%' }}>
                                {
                                    data.map(item => (
                                        <CustomResultCard key={item._id} data={item} />
                                    ))
                                }
                            </ResultCardsWrapper>
                        )}
                    </ReactiveList>
                </div>
            </div>
        </ReactiveBase >

    );
};

export default GoodreadsSearch;

