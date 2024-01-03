import React, { useEffect, useState } from 'react';
import { Reorder, useDragControls, useMotionValue } from 'framer-motion';
import "./Task.scss";
import DeleteBtn from './delete-btn/DeleteBtn';
import { useRaisedShadow } from './useRaisedShadow';
import useDebounce from 'src/components/useDebounce';

interface TaskProps {
    task: {
        id: number;
        title: string;
        completed: boolean;
        position: number;
    };
    onDelete: (id: number) => void;
    onToggleCompleted: (id: number) => void;
    onUpdateTitle: (id: number, title: string) => void;
}

const Task: React.FC<TaskProps> = ({ task, onDelete, onToggleCompleted, onUpdateTitle }) => {
    const controls = useDragControls();
    const y = useMotionValue(0);
    const boxShadow = useRaisedShadow(y);
    const [title, setTitle] = useState(task.title);
    const debouncedTitle = useDebounce(title, 500);

    useEffect(() => {
        if (debouncedTitle !== task.title) {
            onUpdateTitle(task.id, debouncedTitle);
        }
    }, [debouncedTitle, task.id, task.title, onUpdateTitle]);


    return (
        <Reorder.Item
            value={task}
            id={task.id.toString()}
            style={{ boxShadow, y }}
            dragListener={false}
            dragControls={controls}
            className="Task"
        >
            <span className='TaskInnerWrapper'>
                <div>
                    <span
                        className="reorder-handle"
                        onPointerDown={(e) => controls.start(e)}
                    >
                        &#9776;
                    </span>
                    <input type="checkbox" checked={task.completed} onChange={() => onToggleCompleted(task.id)} />
                    <input value={title} onChange={(e)=>{
                        setTitle(e.target.value)
                    }} />
                </div>
                <DeleteBtn onDelete={onDelete} id={task.id} />
            </span>
        </Reorder.Item>
    );
};

export default Task;
