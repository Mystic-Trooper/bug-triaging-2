def calculate_decay_factor(tx, assignee, component):
    # Calculate the average solving time of bugs for this assignee and component
    avg_solving_time = tx.run("MATCH (a:assignee{name: $assignee})<-[:assignedTo]-(b:bugId)-[:belongsToComponent]->(c:component{name: $component}),(b)-[:solvedin]->(s:solving_time) "
                              "RETURN avg(toInteger(s.name)) AS avg_solving_time",
                              assignee=assignee, component=component).single()["avg_solving_time"]

    # Calculate the total decay factor for all bugs resolved by this assignee in this component
    total_decay_factor = 0
    result = tx.run("MATCH (a:assignee{name: $assignee})<-[:assignedTo]-(b:bugId)-[:belongsToComponent]->(c:component{name: $component}),(b)-[e:decay_time]->(d:decay_time) "
                    "RETURN e.weight AS days_diff_from_today",
                    assignee=assignee, component=component)
    for record in result:
        days_diff_from_today = record["days_diff_from_today"]
        if avg_solving_time == 0:
            decay_factor = 0
        else:
            decay_factor = math.exp(-days_diff_from_today / avg_solving_time)
        total_decay_factor += decay_factor

    # Calculate the average decay factor for this assignee in this component
    num_bugs = tx.run("MATCH (a:assignee{name: $assignee})<-[:assignedTo]-(b:bugId)-[:belongsToComponent]->(c:component{name: $component}) "
                      "RETURN count(b) AS num_bugs",
                      assignee=assignee, component=component).single()["num_bugs"]
    if num_bugs == 0:
        avg_decay_factor = 0
    else:
        avg_decay_factor = total_decay_factor / num_bugs

    return avg_decay_factor
