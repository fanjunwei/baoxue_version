CREATE VIEW `v_browse` AS
    select 
        `version_version`.`id` AS `id`,
        `version_version`.`name` AS `version_name`,
        `version_subbranch`.`name` AS `subbranch_name`,
        `version_branch`.`name` AS `branch_name`,
        `version_version`.`fullName` AS `fullName`,
        `version_version`.`createTime` AS `version_createTime`,
        `version_version`.`description` AS `description`,
        `version_version`.`parent` AS `parent`,
        `version_version`.`parentFullName` AS `parentFullName`,
        `version_subbranch`.`description` AS `subbranch_description`,
        `version_branch`.`description` AS `branch_description`
    from
        ((`version_version`
        join `version_subbranch` ON ((`version_version`.`subBranch_id` = `version_subbranch`.`id`)))
        join `version_branch` ON ((`version_subbranch`.`branch_id` = `version_branch`.`id`)))
    order by `version_branch`.`name` , `version_subbranch`.`name` , `version_version`.`createTime`;