import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import TuneIcon from '@mui/icons-material/Tune';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import DesktopDatePicker from '@mui/lab/DesktopDatePicker';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Rating from '@mui/material/Rating';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { format } from 'date-fns';
import React, { useState } from 'react';
import { FormattedMessage } from 'react-intl';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory } from 'react-router-dom';
import * as actions from '../actions';
import * as selectors from '../selectors';


const BookSearch = () => {

    const dispatch = useDispatch();
    const history = useHistory();
    const [title, setTitle] = useState('');
    const [authorName, setAuthorName] = useState('');
    const [genre, setGenre] = useState('');
    const [publicationDate, setPublicationDate] = useState(null);
    const [averageScore, setAverageScore] = useState(0.0);
    const authors = useState('');


    const genres = [
        {
            value: 'SF',
            label: <FormattedMessage id="project.book.genre.SF" />,
        },
        {
            value: 'FA',
            label: <FormattedMessage id="project.book.genre.FA" />,
        },
        {
            value: 'FI',
            label: <FormattedMessage id="project.book.genre.FI" />,
        },
        {
            value: 'HO',
            label: <FormattedMessage id="project.book.genre.HO" />,
        },
        {
            value: 'TH',
            label: <FormattedMessage id="project.book.genre.TH" />,
        },
        {
            value: 'RO',
            label: <FormattedMessage id="project.book.genre.RO" />,
        },
        {
            value: 'BIO',
            label: <FormattedMessage id="project.book.genre.BIO" />,
        },
        {
            value: 'PO',
            label: <FormattedMessage id="project.book.genre.PO" />,
        },
        {
            value: 'MR',
            label: <FormattedMessage id="project.book.genre.MR" />,
        },
        {
            value: 'HI',
            label: <FormattedMessage id="project.book.genre.HI" />,
        },
        {
            value: 'CL',
            label: <FormattedMessage id="project.book.genre.CL" />,
        },
    ];


    const onAuthorNameSelected = (value) => {
        setAuthorName(value);

    }

    const onAuthorNameChanged = (value) => {
        setAuthorName(value);
        if (value.length >= 3) {
            dispatch(actions.getAuthors(value));
        } else {
            if (value === '') {
                dispatch(actions.clearAuthors());
            }

        }
    }

    const handleChangePublicationDate = (newValue) => {
        let date = format(newValue, 'yyyy-MM-dd');
        setPublicationDate(date);
    }

    /*const handleSubmit = event => {
        event.preventDefault();
        dispatch(actions.findBooksByFilters(
            { title, authorName, genre, publicationDate, averageScore }));
        history.push('/books/find-books-by-filters');

    }*/

    const handleDeleteTitle = () => {
        setTitle('');
    }

    const handleDeleteAuthor = () => {
        setAuthorName('');
    }

    const handleDeleteGenre = () => {
        setGenre('');
    }

    const handleDeletePulicationDate = () => {
        setPublicationDate(null);
    }

    const handleDeleteAverageScore = () => {
        setAverageScore(0.0);
    }


    const [anchorEl3, setAnchorEl3] = useState(null);


    const openSearch = Boolean(anchorEl3);

    const stopImmediatePropagation = (e) => {
        e.stopPropagation();
        e.preventDefault();
    };

    const handleClickSearch = (event) => {
        setAnchorEl3(event.currentTarget);
    };
    const handleCloseSearch = () => {
        setAnchorEl3(null);
    };



    return (

        <Stack direction="row" marginBottom={1}>
            <IconButton
                ria-controls={openSearch ? 'basic-menu' : undefined}
                aria-haspopup="true"
                aria-expanded={openSearch ? 'true' : undefined}
                onClick={handleClickSearch}
                sx={{ mr: 0, mt: 1, color: '#FFFFFF' }}
                size="large"
                edge="start"

            >
                <TuneIcon />
            </IconButton>
            <Menu
                MenuListProps={{
                    "aria-labelledby": "basic-button",
                    sx: { width: 335 }
                }}
                id="basic-menu"
                anchorEl={anchorEl3}
                open={openSearch}
                onClose={handleCloseSearch}
            > <Typography variant="h7" fontWeight='bold' sx={{ ml: 8 }}>
                    {<FormattedMessage id="project.books.advancedSearchTitle" />}
                </Typography>
                <MenuItem
                    onKeyDown={e => e.stopPropagation()}>
                    <TextField
                        label={<FormattedMessage id="project.books.title" />}
                        id="title"
                        style={{ margin: 1 }}
                        sx={{ width: 258 }}
                        variant="outlined"
                        margin="normal"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                    />
                    <IconButton color="error"
                        onClick={handleDeleteTitle}>
                        <HighlightOffIcon />
                    </IconButton>
                </MenuItem>
                <MenuItem
                    onKeyDown={e => e.stopPropagation()}>
                    <Autocomplete
                        id="authorName"
                        freeSolo
                        sx={{ width: 258 }}
                        disableClearable
                        autoSelect
                        value={authorName}
                        onChange={(event, value, reason, details) => onAuthorNameSelected(value)}
                        options={authors.map((option) => option.completeName)}
                        renderInput={(params) =>
                            <TextField {...params} style={{ margin: 1 }} onChange={e => onAuthorNameChanged(e.target.value)}
                                sx={{ width: 258 }} label={<FormattedMessage id="project.books.authorName" />}
                            />}
                    />
                    <IconButton color="error"
                        onClick={handleDeleteAuthor}>
                        <HighlightOffIcon />
                    </IconButton>
                </MenuItem>
                <MenuItem sx={{ width: 350 }} onKeyDown={e => e.stopPropagation()}>
                    <TextField sx={{ width: 257 }}
                        margin="none"
                        select
                        id="genre"
                        label={<FormattedMessage id="project.books.genre" />}
                        value={genre}
                        onChange={e => setGenre(e.target.value)}
                    >
                        {genres.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                    <IconButton color="error"
                        onClick={handleDeleteGenre}>
                        <HighlightOffIcon />
                    </IconButton>
                </MenuItem>
                <MenuItem sx={{ width: 350 }} >
                    <LocalizationProvider dateAdapter={AdapterDateFns} >
                        <DesktopDatePicker
                            label={<FormattedMessage id="project.books.publicationDate" />}
                            inputFormat="dd/MM/yyyy"
                            value={publicationDate}
                            onChange={handleChangePublicationDate}
                            renderInput={(params) => <TextField onKeyDown={e => e.preventDefault()}  {...params} />}
                        />

                    </LocalizationProvider>
                    <IconButton color="error"
                        onClick={handleDeletePulicationDate}>
                        <HighlightOffIcon />
                    </IconButton>

                </MenuItem>
                <MenuItem sx={{ width: 258 }}
                >
                    <Typography component="legend" variant="subtitle1" sx={{ mr: 0.75 }}>
                        {<FormattedMessage id="project.books.averageScore" />}</Typography>
                    <Rating
                        name="simple-controlled"
                        precision={0.5}
                        value={averageScore}
                        onChange={e => setAverageScore(e.target.value)}
                    />
                    <IconButton color="error"
                        onClick={handleDeleteAverageScore}>
                        <HighlightOffIcon />
                    </IconButton>

                </MenuItem>


                <div>
                    <MenuItem onClick={handleSubmit}
                    >
                        <Button
                            fullWidth
                            variant='contained'
                        >
                            <Typography  >
                                {<FormattedMessage id="project.global.buttons.search" />}
                            </Typography>
                        </Button>
                    </MenuItem>
                </div>
            </Menu>
        </Stack>
    )
};
export default BookSearch;


