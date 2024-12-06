import {AppBar, Box, Breadcrumbs, CssBaseline, Drawer, styled, Toolbar} from "@mui/material";
import {Link, Outlet, useParams} from "react-router-dom";
import ObjectGrid from "./components/ObjectGrid.tsx";

const StyledBox = styled(Box)`
    display: flex;
`;

const StyledAppBar = styled(AppBar)(({theme}) => ({
    zIndex: theme.zIndex.drawer + 1,
}));

const drawerWidth = 320;

const StyledDrawer = styled(Drawer)`
    width: ${drawerWidth}px;
    flex-shrink: 0;

    & .MuiDrawer-paper {
        width: ${drawerWidth}px;
        box-sizing: border-box;
    }
`;

function App() {
    const {'*': path} = useParams();

    const renderPathBreadcrumb = (path: string) => {
        const parts = path.split('/');
        return parts.map((p, i) => {
            const to = parts.slice(0, i + 1).join('/');
            return (
                <Link to={`bucket/${to}`}>
                    {p}
                </Link>
            );
        });
    }

    return (
        <StyledBox>
            <CssBaseline/>
            <StyledAppBar position="fixed">
                <Toolbar>
                    <Breadcrumbs>
                        <Link to="/">
                            S3 Server
                        </Link>
                        {path && renderPathBreadcrumb(path)}
                    </Breadcrumbs>
                </Toolbar>
            </StyledAppBar>
            <StyledDrawer variant="permanent">
                <Toolbar/>
                <Outlet/>
            </StyledDrawer>
            <Box component="main" sx={{flexGrow: 1, p: 3}}>
                <Toolbar/>
                <ObjectGrid/>
            </Box>
        </StyledBox>
    );
}

export default App
