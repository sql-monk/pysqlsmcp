/*
Get SQL Server wait statistics showing where the server is spending time waiting.
No parameters - returns top wait types by total wait time.
*/

DECLARE
    @dummy INT;

SELECT TOP 20
    wait_type,
    wait_time_ms,
    waiting_tasks_count,
    wait_time_ms / NULLIF(waiting_tasks_count, 0) AS avg_wait_time_ms,
    signal_wait_time_ms,
    wait_time_ms - signal_wait_time_ms AS resource_wait_time_ms
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE', 'SLEEP_TASK',
    'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH', 'WAITFOR', 'LOGMGR_QUEUE',
    'CHECKPOINT_QUEUE', 'REQUEST_FOR_DEADLOCK_SEARCH', 'XE_TIMER_EVENT',
    'BROKER_TO_FLUSH', 'BROKER_TASK_STOP', 'CLR_MANUAL_EVENT',
    'CLR_AUTO_EVENT', 'DISPATCHER_QUEUE_SEMAPHORE', 'FT_IFTS_SCHEDULER_IDLE_WAIT',
    'XE_DISPATCHER_WAIT', 'XE_DISPATCHER_JOIN', 'SQLTRACE_INCREMENTAL_FLUSH_SLEEP'
)
ORDER BY wait_time_ms DESC
