import {List, ListItem, ListItemButton, ListItemIcon, ListItemText} from "@mui/material";
import {useEffect, useState} from "react";
import {ArrowBackOutlined, FolderOutlined} from "@mui/icons-material";
import {Link, useParams} from "react-router-dom";
import {parseBucketName, parseObjectKey} from "../utils.ts";

export default function FolderList() {
    const [folders, setFolders] = useState<string[]>([]);
    const {'*': path} = useParams();
    const bucketName = parseBucketName(path);
    const objectKey = parseObjectKey(path);

    useEffect(() => {
        if (bucketName) {
            const loadBuckets = async () => {
                let url = `/api/v1/buckets/${bucketName}/folders`;
                if (objectKey) {
                    url += `?prefix=${encodeURIComponent(objectKey + '/')}`;
                }
                const res = await fetch(url);
                const json = await res.json();
                setFolders(json.folders);
            };
            loadBuckets();
        }
    }, [bucketName, objectKey]);

    const renderBucketListItem = (folder: string) => {
        return (
            <ListItem key={folder} disablePadding>
                <ListItemButton component={Link} to={`${path}/${folder}`}>
                    <ListItemIcon>
                        <FolderOutlined/>
                    </ListItemIcon>
                    <ListItemText>
                        {folder}
                    </ListItemText>
                </ListItemButton>
            </ListItem>
        );
    }

    const getBackLink = () => {
        let result = '/';
        if (objectKey) {
            result += `bucket/${bucketName}`;
            const folderSeparatorIndex = objectKey.lastIndexOf('/');
            if (folderSeparatorIndex > 0) {
                result += `/${(objectKey.substring(0, folderSeparatorIndex))}`;
            }
        }
        return result;
    }

    const renderBackItem = () => {
        return (
            <ListItem disablePadding>
                <ListItemButton component={Link} to={getBackLink()}>
                    <ListItemIcon>
                        <ArrowBackOutlined/>
                    </ListItemIcon>
                    <ListItemText>
                        Back
                    </ListItemText>
                </ListItemButton>
            </ListItem>
        )
    }

    const renderBucketListItems = () => {
        return folders.map((folder) => renderBucketListItem(folder));
    }

    return (
        <List>
            {renderBackItem()}
            {renderBucketListItems()}
        </List>
    );
}