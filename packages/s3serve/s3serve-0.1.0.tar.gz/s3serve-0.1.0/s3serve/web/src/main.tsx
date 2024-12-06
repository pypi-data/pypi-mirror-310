import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import {createTheme, ThemeProvider} from "@mui/material";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import BucketList from "./components/BucketList.tsx";
import FolderList from "./components/FolderList.tsx";

const theme = createTheme({
    palette: {
        mode: 'dark',
    },
});

const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
        children: [
            {
                path: "/",
                element: <BucketList/>,
            },
            {
                path: "/bucket/*",
                element: <FolderList/>,
            }
        ],
    },
]);

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <ThemeProvider theme={theme}>
            <RouterProvider router={router}/>
        </ThemeProvider>
    </StrictMode>,
);
