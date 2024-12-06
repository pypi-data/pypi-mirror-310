import {List, ListItem, ListItemButton, ListItemIcon, ListItemText} from "@mui/material";
import {useEffect, useState} from "react";
import {CloudCircleOutlined} from "@mui/icons-material";
import {Link} from "react-router-dom";

export default function BucketList() {
    const [buckets, setBuckets] = useState<string[]>([]);

    useEffect(() => {
        const loadBuckets = async () => {
            const res = await fetch('/api/v1/buckets');
            const json = await res.json();
            setBuckets(json.buckets);
        };
        loadBuckets();
    }, []);

    const renderBucketListItem = (bucket: string) => {
        return (
            <ListItem key={bucket} disablePadding>
                <ListItemButton component={Link} to={`bucket/${bucket}`}>
                    <ListItemIcon>
                        <CloudCircleOutlined/>
                    </ListItemIcon>
                    <ListItemText>
                        {bucket}
                    </ListItemText>
                </ListItemButton>
            </ListItem>
        );
    }

    const renderBucketListItems = () => {
        return buckets.map((bucket) => renderBucketListItem(bucket));
    }

    return (
        <List>
            {renderBucketListItems()}
        </List>
    );
}